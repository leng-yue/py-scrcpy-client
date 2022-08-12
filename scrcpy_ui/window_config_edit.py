"""
About UI
    In this file, everyone can be adjusted according to your own needs.
    But should't submit changed code.
"""
import json
import os

from PySide6 import QtCore  # QTranslator
from PySide6.QtGui import QImage, QMouseEvent, QPixmap
from PySide6.QtWidgets import QDialog

from .ui_config_edit import Ui_Dialog


class ConfigEditWindow(QDialog):
    root_dir = ".config"

    def __init__(
        self, name, row, serial_no, signal_config_edit_close=None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        if not serial_no:
            return
        self.row = row
        self.name = name
        self.serial_no = serial_no
        self.signal_config_edit_close = signal_config_edit_close
        self.ui = Ui_Dialog()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 始终最前显示
        self.ui.setupUi(self)

        # event bind
        # self.ui.buttonBox.accepted.connect(self.save_config_info)
        # self.ui.buttonBox.rejected.connect(self.cancel_config_info)

        self.make_config_file_sure()
        for i in [
            self.ui.combobox_ai_level,
            self.ui.combobox_run_mode,
            self.ui.combobox_team,
        ]:
            i.addItems(["aasd", "asdsafjgf", "asdiuguidgqugdqw"])
        self.show_config_info()
        self.show()

    @staticmethod
    def make_config_file_sure():
        if os.path.exists(ConfigEditWindow.root_dir):
            pass
        else:
            os.mkdir(ConfigEditWindow.root_dir)

    @staticmethod
    def get_config_info_from_file(path):
        data = {}
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
        return data

    def get_confg_info(self):
        """
        ret: bool, dict
        """
        data = {
            "team": self.ui.combobox_team.currentText(),
            "ai_level": self.ui.combobox_ai_level.currentText(),
            "account": self.ui.lineedit_account.text(),
            "run_mode": self.ui.combobox_run_mode.currentText(),
            "nickname": self.ui.lineedit_nickname.text(),
            "token": self.ui.textedit_token.toPlainText(),
        }
        for v in data.values():
            if not v:
                return False, None
        return True, data

    def set_combobox(self, combo_widget, text):
        index = 0
        for index in range(combo_widget.count()):
            if combo_widget.itemText(index) == text:
                break
        combo_widget.setCurrentIndex(index)

    def show_config_info(self):
        path = os.path.join(self.root_dir, self.serial_no)
        data = self.get_config_info_from_file(path)
        if data:
            self.set_combobox(self.ui.combobox_team, data["team"])
            self.set_combobox(self.ui.combobox_ai_level, data["ai_level"])
            self.set_combobox(self.ui.combobox_run_mode, data["run_mode"])
            self.ui.lineedit_account.setText(data["account"])
            self.ui.lineedit_nickname.setText(data["nickname"])
            self.ui.textedit_token.setText(data["token"])

    def accept(self):
        print("I'm alive!!!!!")
        can_save, data = self.get_confg_info()
        if not can_save:
            pass
        else:
            path = os.path.join(self.root_dir, self.serial_no)
            with open(path, "w") as f:
                json.dump(data, f)
            self.ignore_flag = False
            self.signal_config_edit_close.emit(self.row, self.serial_no)
            return QDialog.accept(self)

    def reject(self):
        print("I'm cencel!!!!!")
        self.signal_config_edit_close.emit(self.row, self.serial_no)
        QDialog.reject(self)

    def closeEvent(self, _):
        print("close~~~~edit~~~~~")
        self.signal_config_edit_close.emit(self.row, self.serial_no)
