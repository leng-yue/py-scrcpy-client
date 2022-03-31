import numpy as np
from PySide6 import QtCore  # QTranslator
from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QDialog

import scrcpy
from workers import ThreadWorker

from .ui_screen import Ui_Dialog


class ScreenWindow(QDialog):
    signal_frame = Signal(np.ndarray)

    def __init__(self, name, row, serial_no, signal_screen_close=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not serial_no:
            return
        self.signal_screen_close = signal_screen_close
        self.row = row
        self.serial_no = serial_no
        self.ui = Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 始终最前显示
        self.ui.setupUi(self)

        self.max_width = 640
        self.serial_no = serial_no
        # # show
        # self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)

        # show
        self.signal_frame.connect(self.on_frame)
        # Bind mouse event
        self.ui.label_video.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label_video.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label_video.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        self.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", name, None))
        self.tworker = ThreadWorker(0, self.serial_no, signal=self.signal_frame)
        self.show()

    def on_frame(self, frame):
        # app.processEvents()
        # print("frame~~~~")
        if frame is not None:
            # ratio = self.max_width / max(self.client.resolution)
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format_BGR888,
            )
            pix = QPixmap(image)
            # pix.setDevicePixelRatio(1 / ratio)
            self.ui.label_video.setPixmap(pix)
            self.resize(1, 1)

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            ratio = self.max_width / max(self.tworker.client.resolution)
            self.tworker.client.control.touch(
                evt.position().x() - (self.ui.label_video.geometry().x() / 2) / ratio,
                evt.position().y() - (self.ui.label_video.geometry().y() / 2) / ratio,
                action,
            )

        return handler

    def reject(self):
        print("reject~&close~")
        self.close()

    def closeEvent(self, _):
        print("close~~~~")
        self.tworker.stop()
        self.signal_screen_close.emit(self.row, self.serial_no)

    # def showWindow(self):
    #     print("移动", self.x(), self.y())
    #     self.move(int(self.x()), int(self.y()))
