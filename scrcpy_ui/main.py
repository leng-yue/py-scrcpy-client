import os
import sys

from adbutils import adb
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableWidgetItem,
    QWidget,
)

from .config_edit import ConfigEditWindow
from .schemas import runmode
from .screen import ScreenWindow
from .ui_main import Ui_MainWindow
from .worker import ThreadWorker

app = QApplication([])


class MainWindow(QMainWindow):
    signal_screen_close = Signal(int, str)
    signal_config_edit_close = Signal(int, str)

    def __init__(self, account_info=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # bind events
        self.ui.checkbox_devices.clicked.connect(self.on_click_check_all)
        self.ui.button_all_satrt.clicked.connect(self.on_click_all_start)
        self.ui.button_all_stop.clicked.connect(self.on_click_all_stop)

        self.ui.table_devices.horizontalHeader().setStretchLastSection(True)
        self.ui.table_devices.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )  # noEdit
        self.ui.table_devices.setSelectionMode(
            QAbstractItemView.NoSelection
        )  # noSelection
        self.dict_client = {}
        self.dict_window_screen = {}
        self.dict_window_edit = {}

        # UI Text Dict
        self.dict_ui_text = {
            "device_nick_name": {
                "QV7141QF1T": "Xperia1",
                "9LJZQCJFCYUWAM7S": "测试神机001",
            },
            "buttons": {
                # 传入状态(运行时可关闭.关闭时可运行)
                "operate": {1: "停止", -1: "启动"},
                "show": {1: "关闭画面", -1: "显示画面"},
                "edit": {1: "取消编辑", -1: "编辑"},
            },
        }
        self.dict_table_buttons = {}
        self.dict_table_box = {"check": {}, "combo": {}}
        self.update_table_data(data=self.get_table_data())

        # close screnn window
        self.signal_screen_close.connect(self.close_all_about_show)
        self.signal_config_edit_close.connect(self.close_all_about_edit_show)
        self.show()

    def get_device_nick_name(self, serial):
        data = ConfigEditWindow.get_config_info_from_file(
            os.path.join(ConfigEditWindow.root_dir, serial)
        )
        return data.get("nickname") if data else ""

    def get_table_data(self):
        data = []
        for i in adb.device_list():
            serial = i.serial
            data.append(
                [
                    self.check_box_widget,
                    self.get_device_nick_name(serial=serial),
                    serial,
                    "pvp",
                    self.operate_button_widget,
                    self.others_buttons_widget,
                ]
            )
        data.append(
            [
                self.check_box_widget,
                "常驻测试",
                "fake_device",
                "pvp",
                "无法启动",
                self.others_buttons_widget,
            ]
        )
        return data

    # region widgets数据缓存
    def add_button2table_dict(self, row, data):
        if not self.dict_table_buttons.get(row):
            self.dict_table_buttons[row] = {}
        self.dict_table_buttons[row].update(data)

    def chg_button2table_dict(self, row, name, status):
        row_data = self.dict_table_buttons.get(row)
        if row_data:
            if status > 0:
                row_data[name].setStyleSheet(
                    """ text-align : center;
                        background-color : LightCoral;
                        """
                )
            else:
                row_data[name].setStyleSheet("")
            row_data[name].setText(self.dict_ui_text["buttons"][name][status])

    def add_box2table_dict(self, row, name, box_widget):
        """
        保存 box 组建:
        name str in( check, combo )
        """
        self.dict_table_box[name][row] = box_widget

    def chg_box2table_dict(self, row, reverse=True, sure=0, checkbox=None):
        """
        修改checkbox 状态
        reverse: 将当前状态反转
        sure: 1 勾选, -1 取消勾选
        """
        if row and not checkbox:
            checkbox = self.dict_table_box["check"].get(row)
        if reverse:
            _status = checkbox.isChecked()
            checkbox.setChecked(not _status)
        elif sure:
            checkbox.setChecked(sure > 0)

    # endregion

    # region 特殊Table 元素
    def combo_box_widget(self, row):
        combobox = QComboBox()
        combobox.addItems(runmode.All)
        self.add_box2table_dict(row, "combo", combobox)
        return combobox

    def check_box_widget(self, row):
        checkbox = QCheckBox()
        self.add_box2table_dict(row, "check", checkbox)
        return checkbox

    def operate_button_widget(self, row):
        button = QPushButton(self.dict_ui_text["buttons"]["operate"][-1])
        button.clicked.connect(self.on_click_operate)
        data = {"operate": button}
        self.add_button2table_dict(row, data)
        return button

    def others_buttons_widget(self, row):
        widget = QWidget()
        hlayout = QHBoxLayout()
        button_edit = QPushButton("编辑")
        button_edit.clicked.connect(self.on_click_edit)
        # button_edit.setStyleSheet(
        #     """ text-align : center;
        #         background-color : NavajoWhite;
        #         height : 30px;
        #         border-style: outset;
        #         font : 13px  """
        # )
        # button_cpy = QPushButton("复制")
        # button_cpy.clicked.connect(self.on_click_cpy)
        button_show = QPushButton(self.dict_ui_text["buttons"]["show"][-1])
        button_show.clicked.connect(self.on_click_show)
        hlayout.addWidget(button_edit)
        # hlayout.addWidget(button_cpy)
        # hlayout.addWidget(button_del)
        hlayout.addWidget(button_show)
        self.add_button2table_dict(row, {"edit": button_edit, "show": button_show})
        hlayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hlayout)
        return widget

    # endregion

    # region 事件处理

    def on_click_all_start(self):
        for row, box in self.dict_table_box["check"].items():
            row, _, serial_no = self.get_table_row_info(row)
            if box.isChecked() and not self.dict_client.get(serial_no):
                self.on_click_operate(row=row, serial_no=serial_no)

    def on_click_all_stop(self):
        for row, box in self.dict_table_box["check"].items():
            row, _, serial_no = self.get_table_row_info(row)
            if box.isChecked() and self.dict_client.get(serial_no):
                self.on_click_operate(row=row, serial_no=serial_no)

    def on_click_check_all(self):
        for row, box in self.dict_table_box["check"].items():
            if self.ui.checkbox_devices.isChecked():
                self.chg_box2table_dict(row, sure=1, checkbox=box)
            else:
                self.chg_box2table_dict(row, sure=-1, checkbox=box)

    def get_table_row_info(self, row):
        serial_no = self.ui.table_devices.item(row, 2).text()
        name = self.ui.table_devices.item(row, 1).text()
        return row, name, serial_no

    def get_table_row_info_by_button(self, by_parent_pos=False):
        """
        通过点击的button所在位置/button‘s parent所在位置获取当前行信息
        ret: tuple[str]
            row, name, serial_no
        """
        button = self.sender()
        if button:
            if by_parent_pos:
                row = self.ui.table_devices.indexAt(button.parent().pos()).row()
            else:
                row = self.ui.table_devices.indexAt(button.pos()).row()
            return self.get_table_row_info(row)

    def on_click_edit(self):
        row, name, serial_no = self.get_table_row_info_by_button(by_parent_pos=True)
        win_edit = self.dict_window_edit.get(serial_no)
        self.chg_button2table_dict(row, "edit", 1)
        if not win_edit:
            _win_edit = ConfigEditWindow(
                name, row, serial_no, self.signal_config_edit_close
            )
            self.dict_window_edit[serial_no] = _win_edit
        else:
            win_edit.close()

    # def on_click_cpy(self):
    #     pass

    def close_all_about_edit_show(self, row, serial_no):
        del self.dict_window_edit[serial_no]
        self.chg_button2table_dict(row, "edit", -1)

    def close_all_about_show(self, row, serial_no):
        del self.dict_window_screen[serial_no]
        self.chg_button2table_dict(row, "show", -1)

    def on_click_show(self):
        row, name, serial_no = self.get_table_row_info_by_button(by_parent_pos=True)
        win_screen = self.dict_window_screen.get(serial_no)
        if not win_screen:
            _win_screen = ScreenWindow(name, row, serial_no, self.signal_screen_close)
            self.dict_window_screen[serial_no] = _win_screen
            self.dict_window_screen[serial_no].tworker.start()
            self.chg_button2table_dict(row, "show", 1)
            # self.dict_window_screen[serial_no].showWindow()
        else:
            win_screen.close()
            # self.close_all_about_show(row, serial_no)

    def on_click_operate(self, row=None, serial_no=None):
        if isinstance(row, int) and serial_no:
            pass
        elif isinstance(row, int):
            row, _, serial_no = self.get_table_row_info(row=row)
        else:
            row, _, serial_no = self.get_table_row_info_by_button()
        client = self.dict_client.get(serial_no)
        if not client:
            tworker = ThreadWorker(row, serial_no)
            self.dict_client[serial_no] = tworker
            self.dict_client[serial_no].start()
            self.chg_button2table_dict(row, "operate", 1)
        else:
            client.stop()
            del self.dict_client[serial_no]
            self.chg_button2table_dict(row, "operate", -1)

    def update_table_data(self, data):
        self.dict_table_buttons = {}
        self.dict_table_box = {"check": {}, "combo": {}}
        for item in data:
            row = self.ui.table_devices.rowCount()
            self.ui.table_devices.insertRow(row)
            for j, v in enumerate(item):
                if isinstance(v, type(self.update_table_data)):
                    func_data = v(row)
                    self.ui.table_devices.setCellWidget(row, j, func_data)
                else:
                    v = QTableWidgetItem(v)
                    self.ui.table_devices.setItem(row, j, v)

    def closeEvent(self, event: QCloseEvent) -> None:
        for _, client in self.dict_client.items():
            client.stop()
        return super().closeEvent(event)

    # endregion


def main():
    # dialog = LoginDialog()
    # if dialog.exec() == QDialog.Accepted:
    #     m = MainWindow(dialog.account_info)
    #     m.show()

    # s = ScreenWindow()
    # s.show()
    m = MainWindow()
    m.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
