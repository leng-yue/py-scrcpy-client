import datetime
import json
import os

import PySide6
from PySide6.QtCore import Signal, Qt, QRectF, QObject, QTimer
from PySide6.QtGui import QPixmap, QPen, QColor
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsItem,
    QGraphicsPixmapItem,
    QWidget,
    QMessageBox,
)

from scrcpy_ui.logger import Logger
from scrcpy_ui.region_save_dialog import RegionSaveDialog
from .ui import Ui_FrameViewer


class GraphicsView(QGraphicsView):
    save_signal = Signal(bool)
    onImageSet = Signal(QPixmap)
    onZoom = Signal(float)

    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        # 设置放大缩小时跟随鼠标
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # 设置空白背景
        self.image_item = GraphicsPixmapItem(QPixmap())
        self.image_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.scene.addItem(self.image_item)

        size = self.image_item.pixmap().size()
        # 调整图片在中间
        self.image_item.setPos(-size.width() / 2, -size.height() / 2)
        # self.scale(0.1, 0.1)

    def set_image(self, image):
        self.image_item.setPixmap(image)
        size = self.image_item.pixmap().size()
        self.image_item.setPos(-size.width() / 2, -size.height() / 2)
        self.onImageSet.emit(self.image_item.pixmap())
        # self.scale(1, 1)

    def wheelEvent(self, event):
        """滚轮事件"""
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor

        self.scale(zoomFactor, zoomFactor)
        self.onZoom.emit(zoomFactor)

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        # print(self.image_item.is_finish_cut, self.image_item.is_start_cut)
        if self.image_item.is_finish_cut:
            self.save_signal.emit(True)
        else:
            self.save_signal.emit(False)


class GraphicsPixmapItem(QGraphicsPixmapItem, QObject):
    save_signal = Signal(bool)

    def __init__(self, picture, parent=None):
        super(GraphicsPixmapItem, self).__init__(parent)

        self.end_point = None
        self.is_midbutton = None
        self.start_point = None
        self.setPixmap(picture)
        self.is_start_cut = False
        self.current_point = None
        self.is_finish_cut = False

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        self.current_point = event.pos()
        if not self.is_start_cut or self.is_midbutton:
            self.moveBy(
                self.current_point.x() - self.start_point.x(),
                self.current_point.y() - self.start_point.y(),
            )
            self.is_finish_cut = False
        self.update()

    def mousePressEvent(self, event):
        """鼠标按压事件"""
        super(GraphicsPixmapItem, self).mousePressEvent(event)
        self.start_point = event.pos()
        self.current_point = None
        self.is_finish_cut = False
        if event.button() == Qt.MouseButton.MiddleButton:
            self.is_midbutton = True
            self.update()
        else:
            self.is_midbutton = False
            self.update()

    def paint(self, painter, QStyleOptionGraphicsItem, QWidget):
        super(GraphicsPixmapItem, self).paint(
            painter, QStyleOptionGraphicsItem, QWidget
        )
        if self.is_start_cut and not self.is_midbutton:
            # print(self.start_point, self.current_point)
            pen = QPen(Qt.DashLine)
            pen.setColor(QColor(0, 150, 0, 70))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(QColor(0, 0, 255, 70))
            if not self.current_point:
                return
            painter.drawRect(QRectF(self.start_point, self.current_point))
            self.end_point = self.current_point
            self.is_finish_cut = True


class FrameViewer(QWidget):
    counter = 0

    def __init__(self):
        super().__init__()
        self.ui = Ui_FrameViewer(GraphicsView)
        self.ui.setupUi(self)

        view: GraphicsView = self.ui.graphicsView
        view.onImageSet.connect(self.on_image_set)
        view.onZoom.connect(self.on_zoom)

        self.ui.button_take_region.clicked.connect(self.on_click_take_region)
        self.ui.button_cancel_region.clicked.connect(self.on_click_cancel_region)
        self.ui.button_save_region.clicked.connect(self.on_click_save_region)

        self.check_point_timer = None
        self.clean_point_labels_text()

        self.setWindowTitle("FrameViewer")

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.deleteLater()
        super().closeEvent(event)

    def set_pixmap(self, image: QPixmap):
        self.ui.graphicsView.set_image(image)

    def on_image_set(self, image: QPixmap):
        self.ui.label_picture_resolution.setText(f"{image.width()}x{image.height()}")
        self.ui.label_picture_zoom.setText(f"{1.0:.2f}")

        if self.check_point_timer is not None:
            self.check_point_timer.stop()
            self.check_point_timer.timeout.disconnect(self.on_timeout)
            self.check_point_timer.deleteLater()

        self.check_point_timer = QTimer()
        self.check_point_timer.setInterval(50)
        self.check_point_timer.setSingleShot(False)
        self.check_point_timer.timeout.connect(self.on_timeout)
        self.check_point_timer.start()
        Logger.success("图片加载成功", self)

    def on_zoom(self, zoom: float):
        self.ui.label_picture_zoom.setText(
            f"{zoom * float(self.ui.label_picture_zoom.text()):.2f}"
        )

    def on_click_take_region(self):
        self.ui.graphicsView.image_item.is_start_cut = True
        self.ui.graphicsView.image_item.is_finish_cut = False
        self.ui.graphicsView.image_item.update()
        Logger.info("开始选区", self)

    def on_click_cancel_region(self):
        self.ui.graphicsView.image_item.is_start_cut = False
        self.ui.graphicsView.image_item.is_finish_cut = False
        self.ui.graphicsView.image_item.update()
        Logger.info("取消选区", self)

    def clean_point_labels_text(self):
        self.ui.label_region_point1.setText("-1, -1")
        self.ui.label_region_point2.setText("-1, -1")
        self.ui.label_region_size.setText("-1, -1")

    def on_click_save_region(self):
        point1 = self.ui.graphicsView.image_item.start_point
        point2 = self.ui.graphicsView.image_item.end_point
        if point1 is None or point2 is None:
            print("no region selected")
            return
        x1, y1 = int(point1.x()), int(point1.y())
        x2, y2 = int(point2.x()), int(point2.y())
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self.save_region(x1, y1, x2, y2)
        self.ui.graphicsView.image_item.is_start_cut = False
        self.ui.graphicsView.image_item.is_finish_cut = True
        self.ui.graphicsView.image_item.update()

    def save_region(self, x1: int, y1: int, x2: int, y2: int):
        resolution = self.ui.label_picture_resolution.text()
        width, height = resolution.split("x")
        width, height = int(width), int(height)
        default_name = f"region_{self.counter}"

        pixmap = self.ui.graphicsView.image_item.pixmap()
        pixmap = pixmap.copy(x1, y1, x2 - x1, y2 - y1)

        region_name = RegionSaveDialog.show_dialog(
            resolution=(width, height),
            point1=(x1, y1),
            point2=(x2, y2),
            region_size=(x2 - x1, y2 - y1),
            pixmap=pixmap,
            default_name=default_name,
        )
        if region_name is None:
            Logger.info("取消保存选区", self)
            return
        if region_name == default_name:
            self.counter += 1
        os.makedirs("regions", exist_ok=True)
        pixmap.save(f"regions/{region_name}.png")
        with open(f"regions/regions.txt", "a") as f:
            data = json.dumps(
                {
                    "name": region_name,
                    "point1": [x1, y1],
                    "point2": [x2, y2],
                    "size": [x2 - x1, y2 - y1],
                    "resolution": [width, height],
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[
                        :-3
                    ],
                },
                ensure_ascii=False,
            )
            f.write(data + "\n")
        QMessageBox.information(self, "保存成功", f"保存成功, 保存为regions/{region_name}.png")
        Logger.success(f"保存成功, 保存为regions/{region_name}.png", self)

    def on_timeout(self):
        self.on_start_point_changed()
        self.on_end_point_changed()

    def on_start_point_changed(self):
        try:
            point = self.ui.graphicsView.image_item.start_point
        except AttributeError:
            return None
        if point is None:
            return
        x, y = point.x(), point.y()
        self.ui.label_region_point1.setText(f"{x:.0f}, {y:.0f}")

    def on_end_point_changed(self):
        try:
            point = self.ui.graphicsView.image_item.end_point
        except AttributeError:
            return None
        if point is None:
            return
        self.ui.label_region_point2.setText(f"{point.x():.0f}, {point.y():.0f}")
        region_size = (
            self.ui.graphicsView.image_item.end_point
            - self.ui.graphicsView.image_item.start_point
        )
        self.ui.label_region_size.setText(
            f"{abs(region_size.x()):.0f}, {abs(region_size.y()):.0f}"
        )


def profile_func(frame, event, arg):
    print(frame, event, arg)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    view = FrameViewer()
    view.ui.graphicsView.set_image(QPixmap("img.png"))
    view.show()
    sys.exit(app.exec())
