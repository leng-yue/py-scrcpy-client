from PySide6 import QtCore  # QTranslator
from PySide6.QtGui import QImage, QMouseEvent, QPixmap
from PySide6.QtWidgets import QDialog

from .ui_config_edit import Ui_Dialog


class ConfigEditWindow(QDialog):
    def __init__(self, name, row, serial_no, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not serial_no:
            return
        self.name = name
        self.serial_no = serial_no
        self.ui = Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 始终最前显示
        self.ui.setupUi(self)
        self.show()

    def closeEvent(self, _):
        print("close~~~~")
        # self.signal_screen_close.emit(self.row, self.serial_no)
