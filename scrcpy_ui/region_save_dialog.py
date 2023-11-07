from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from .ui import Ui_RegionSaveDialog


class RegionSaveDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegionSaveDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setText("保存")
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("取消")
        self.setWindowTitle("保存选区")

    def exec0(self):
        ret = self.exec()
        if ret == QDialog.DialogCode.Accepted:
            region_name = (
                self.ui.line_edit_region_name.placeholderText()
                or self.ui.line_edit_region_name.text()
            )
            return region_name
        else:
            return None

    @staticmethod
    def show_dialog(
        resolution: tuple[int, int],
        point1: tuple[int, int],
        point2: tuple[int, int],
        region_size: tuple[int, int],
        pixmap: QPixmap,
        default_name: str = "",
    ):
        instance = RegionSaveDialog()
        instance.ui.label_resolution.setText(f"{resolution[0]}x{resolution[1]}")
        instance.ui.label_point1.setText(f"{point1[0]}, {point1[1]}")
        instance.ui.label_point2.setText(f"{point2[0]}, {point2[1]}")
        instance.ui.label_region_size.setText(f"{region_size[0]}x{region_size[1]}")
        instance.ui.image_display.setPixmap(pixmap)
        instance.ui.line_edit_region_name.setPlaceholderText(default_name)
        return instance.exec0()
