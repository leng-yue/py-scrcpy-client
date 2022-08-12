import os
import threading
import time
from multiprocessing import Process

from adbutils import adb
from loguru import logger
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTableWidgetItem,
    QWidget,
)

from workers import ThreadWorker, UDPServer
from workers.schemas import ServerInfo

from .schemas import runmode
from .ui_main import Ui_MainWindow
from .window_config_edit import ConfigEditWindow
from .window_screen import ScreenWindow


class MainWindow(QMainWindow):
    signal_screen_close = Signal(int, str)
    signal_config_edit_close = Signal(int, str)
    signal_update_table = Signal(list, list)

    def __init__(self, account_info=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.SerialColNum = 0
        # sub process
        self.serverinfo = ServerInfo(host="127.0.0.1", port=9090)
        self.subprocess = Process(
            target=UDPServer().run, args=(self.serverinfo.host, self.serverinfo.port)
        )
        self.subprocess.start()
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
            "buttons": {
                # 传入状态(运行时可关闭.关闭时可运行)
                "operate": {1: "停止", -1: "启动"},
                "show": {1: "关闭画面", -1: "显示画面"},
                "edit": {1: "取消编辑", -1: "编辑"},
            },
        }
        self.dict_table_buttons = {}
        self.dict_table_box = {"check": {}, "combo": {}}
        # self.update_table_data(data=self.get_table_data())

        # close screnn window
        self.signal_screen_close.connect(self.close_all_about_show)
        self.signal_config_edit_close.connect(self.close_all_about_edit_show)
        self.show()

        # region threads
        threading.Thread(
            target=self.listen_device, args=(self.signal_update_table,), daemon=True
        ).start()
        self.signal_update_table.connect(self.update_table_data)
        # threading.Thread(target=self.reconnect_offline, daemon=True).start()
        # endregion

    def get_device_nick_name(self, serial):
        data = ConfigEditWindow.get_config_info_from_file(
            os.path.join(ConfigEditWindow.root_dir, serial)
        )
        return data.get("nickname") if data else ""

    def get_table_data(self):
        data = []
        self.SerialColNum = 2
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
    def listen_device(self, signal):
        while True:
            data = self.get_table_data()
            all_serials = {d[2] for d in data}
            rows = self.ui.table_devices.rowCount()
            if not rows:
                time.sleep(2)
                rows = 1
            old_serials_map = {
                self.ui.table_devices.item(row, 2).text(): row
                for row in range(rows)
                if self.ui.table_devices.item(row, 2)
            }
            old_serials = set(old_serials_map.keys())
            keep = all_serials & old_serials
            to_insert_data = [d for d in data if d[2] not in keep]
            if to_insert_data:
                print("to insert", to_insert_data)
            to_remove = [se for se in old_serials if se not in keep]
            if to_insert_data or to_remove:
                signal.emit(to_insert_data, to_remove)
            time.sleep(2)

    # def reconnect_offline(self):
    #     import subprocess

    #     while True:
    #         time.sleep(5)
    #         try:
    #             to_reconnect_devices = []
    #             path = adb_path()
    #             try:
    #                 sys._MEIPASS
    #                 path = os.path.join("adbutils", "binaries", "adb.exe")
    #             except:
    #                 pass
    #             encoding = "utf-8"
    #             if sys.platform == "win32":
    #                 encoding = "gbk"
    #             res = subprocess.Popen(
    #                 "{} devices -l".format(path),
    #                 shell=True,
    #                 stdout=subprocess.PIPE,
    #                 encoding=encoding,
    #             )
    #             try:
    #                 res, _ = res.communicate(timeout=3)
    #             except Exception as e:
    #                 logger.error(
    #                     "{} error {}".format("{} devices -l".format(path), str(e))
    #                 )
    #                 continue

    #             for line in res.split("\n"):
    #                 line = line.strip()
    #                 if line.startswith("emulator") or not line:
    #                     continue
    #                 if "offline" in line:
    #                     res_list = line.split(" ")
    #                     device_sn = res_list[0]
    #                     to_reconnect_devices.append(device_sn)
    #             if to_reconnect_devices:
    #                 logger.info("to_reconnect_devices: {}".format(to_reconnect_devices))
    #             for device_sn in to_reconnect_devices:
    #                 subprocess.Popen(
    #                     "{} disconnect {}".format(path, device_sn), shell=True
    #                 )
    #                 subprocess.Popen(
    #                     "{} connect {}".format(path, device_sn), shell=True
    #                 )
    #                 logger.debug("{} connect {}".format(path, device_sn))
    #         except Exception as e:
    #             logger.error("reconnect error: {}".format(str(e)))

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
            tworker = ThreadWorker(row, serial_no, serverinfo=self.serverinfo)
            self.dict_client[serial_no] = tworker
            self.dict_client[serial_no].start()
            self.chg_button2table_dict(row, "operate", 1)
        else:
            client.stop()
            del self.dict_client[serial_no]
            self.chg_button2table_dict(row, "operate", -1)

    def update_table_data(self, data: list, remove_serialno: list = None):
        logger.warning(f"数据刷新: {data}\n \t\t{remove_serialno}")
        self.dict_table_buttons = {}
        self.dict_table_box = {"check": {}, "combo": {}}
        for _rm_no in remove_serialno:
            logger.info(
                f"self.ui.table_devices.rowCount(): {self.ui.table_devices.rowCount()}\n self.ui.table_devices.item(row_num, self.SerialColNum): {self.ui.table_devices.item(0, self.SerialColNum).text()}"
            )
            for row_num in range(self.ui.table_devices.rowCount()):
                if (
                    self.ui.table_devices.item(row_num, self.SerialColNum).text()
                    in remove_serialno
                ):
                    logger.warning(f"will remove row: {row_num}, no: {_rm_no}")
                    self.ui.table_devices.removeRow(row_num)

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
        self.subprocess.kill()
        return super().closeEvent(event)

    # endregion
