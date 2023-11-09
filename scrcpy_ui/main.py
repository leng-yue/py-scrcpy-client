import queue
import time
from argparse import ArgumentParser
from typing import Optional

import numpy as np
from PySide6 import QtCore
from PySide6.QtCore import QPoint
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap, QWheelEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from adbutils import adb

import scrcpy
from .frame_viewer import FrameViewer
from .logger import Logger
from .ui import Ui_MainWindow
from .utils.mouse_recorder import MouseRecorder


def get_formatted_bitrate(bitrate):
    if bitrate < 2**10:
        return f"{bitrate} bps"
    elif bitrate < 2**20:
        return f"{bitrate / 2 ** 10:.2f} Kbps"
    elif bitrate < 2**30:
        return f"{bitrate / 2 ** 20:.2f} Mbps"
    else:
        return f"{bitrate / 2 ** 30:.2f} Gbps"


class MainWindow(QMainWindow):
    onMouseReleased = QtCore.Signal(QPoint)

    def __init__(
        self,
        max_width: Optional[int],
        serial: Optional[str] = None,
        encoder_name: Optional[str] = None,
        max_fps: Optional[int] = None,
        bitrate: Optional[int] = None,
    ):
        super(MainWindow, self).__init__()
        self.serial = serial
        self.__frame_time_window = queue.Queue(30)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.max_width = max_width
        self.logger = Logger.get_logger()

        # Setup devices
        self.devices = self.list_devices()
        if serial:
            self.choose_device(serial)
        self.device = adb.device(serial=self.ui.combo_device.currentText())
        self.alive = True

        # Setup client
        self.client = scrcpy.Client(
            device=self.device,
            flip=self.ui.flip.isChecked(),
            bitrate=bitrate or 1_000_000_000,
            max_fps=max_fps or 30,
            encoder_name=encoder_name,
        )
        self.client.add_listener(scrcpy.EVENT_INIT, self.on_init)
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)

        # Setup developer tools
        self.mouse_recorder = MouseRecorder(self.client)
        self.onMouseReleased.connect(self.mouse_recorder.on_mouse_released)

        # Bind controllers
        self.ui.button_home.clicked.connect(self.on_click_home)
        self.ui.button_back.clicked.connect(self.on_click_back)
        self.ui.button_switch.clicked.connect(self.on_click_switch)

        self.ui.button_record_click.clicked.connect(self.on_click_record_click)
        self.ui.button_take_region.clicked.connect(self.on_click_take_region_screenshot)
        self.ui.button_show_log.clicked.connect(self.logger.show)

        self.ui.button_screen_on.clicked.connect(self.on_click_screen_on)
        self.ui.button_screen_off.clicked.connect(self.on_click_screen_off)

        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.flip.stateChanged.connect(self.on_flip)

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)
        self.ui.label.wheelEvent = self.on_mouse_wheel_event

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

        # setup ui elements
        bitrate = self.client.bitrate
        self.ui.label_rate.setText(get_formatted_bitrate(bitrate))
        self.ui.label_encoder.setText(self.client.encoder_name or "Auto")
        # move to left top
        self.move(0, 0)

        # region selector
        self.region_selector = None

        # video player
        # self.video_player = None
        # self.video_widget = QVideoWidget()
        # self.video_widget.setFixedSize(1280, 720)
        # self.video_widget.show()

    def choose_device(self, device):
        if device not in self.devices:
            msgBox = QMessageBox()
            msgBox.setText(f"Device serial [{device}] not found!")
            msgBox.exec()
            return

        # Ensure text
        self.ui.combo_device.setCurrentText(device)
        # Restart service
        if getattr(self, "client", None):
            self.client.stop()
            self.client.device = adb.device(serial=device)
            self.serial = device

    def list_devices(self):
        self.ui.combo_device.clear()
        items = [i.serial for i in adb.device_list()]
        self.ui.combo_device.addItems(items)
        return items

    def on_flip(self, _):
        self.client.flip = self.ui.flip.isChecked()

    def on_click_home(self):
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)
        self.logger.info("Home clicked")

    def on_click_back(self):
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)
        self.logger.info("Back clicked")

    def on_click_switch(self):
        self.client.control.keycode(scrcpy.KEYCODE_APP_SWITCH, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_APP_SWITCH, scrcpy.ACTION_UP)
        self.logger.info("Switch clicked")

    def on_click_screen_on(self):
        # enable phone screen
        self.client.control.set_screen_power_mode(scrcpy.POWER_MODE_NORMAL)

    def on_click_screen_off(self):
        # disable screen
        self.client.control.set_screen_power_mode(scrcpy.POWER_MODE_OFF)

    def on_click_record_click(self):
        if not self.mouse_recorder.is_recording:
            self.mouse_recorder.start_record()
            self.ui.button_record_click.setText("Stop Recording Clicks")
            print(self.ui.button_record_click.styleSheet())
            self.ui.button_record_click.setStyleSheet("background-color: red")
            self.logger.info("Start record click event", self.mouse_recorder)
        else:
            self.mouse_recorder.stop_record()
            self.ui.button_record_click.setText("Start Recording Clicks")
            self.ui.button_record_click.setStyleSheet("background-color: green")
            self.logger.info("Stop record click event", self.mouse_recorder)
            QMessageBox.information(
                self,
                "鼠标记录",
                f"鼠标记录已经保存在{self.mouse_recorder.save_dir}目录下的mouse_records.txt中",
            )

    def on_click_take_region_screenshot(self):
        self.region_selector = FrameViewer()
        self.region_selector.show()
        frame = self.client.last_frame.copy()
        image = QImage(
            frame,
            frame.shape[1],
            frame.shape[0],
            frame.shape[1] * 3,
            QImage.Format_BGR888,
        )
        pix = QPixmap(image)
        self.region_selector.set_pixmap(pix)
        del frame, image, pix

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            ratio = self.max_width / max(self.client.resolution)
            self.client.control.touch(
                evt.position().x() / ratio, evt.position().y() / ratio, action
            )
            pos = QPoint(
                round(evt.position().x() / ratio), round(evt.position().y() / ratio)
            )
            self.on_mouse_moved(pos)

            # if is release, call on_mouse_released
            if action == scrcpy.ACTION_UP:
                self.onMouseReleased.emit(pos)

        return handler

    def on_mouse_wheel_event(self, evt: QWheelEvent):
        start_pos = evt.position()
        ratio = self.max_width / max(self.client.resolution)
        self.client.control.scroll(
            start_pos.x() / ratio,
            start_pos.y() / ratio,
            0,
            evt.angleDelta().y() / 60,
        )

    def on_mouse_moved(self, pos: QPoint):
        # update ui
        self.ui.label_mouse_pos.setText(f"{pos.x()}, {pos.y()}")

    def on_key_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QKeyEvent):
            code = self.map_code(evt.key())
            if code != -1:
                self.client.control.keycode(code, action)

        return handler

    def map_code(self, code):
        """
        Map qt keycode ti android keycode

        Args:
            code: qt keycode
            android keycode, -1 if not founded
        """

        if code == -1:
            return -1
        if 48 <= code <= 57:
            return code - 48 + 7
        if 65 <= code <= 90:
            return code - 65 + 29
        if 97 <= code <= 122:
            return code - 97 + 29

        hard_code = {
            32: scrcpy.KEYCODE_SPACE,
            16777219: scrcpy.KEYCODE_DEL,
            16777248: scrcpy.KEYCODE_SHIFT_LEFT,
            16777220: scrcpy.KEYCODE_ENTER,
            16777217: scrcpy.KEYCODE_TAB,
            16777249: scrcpy.KEYCODE_CTRL_LEFT,
        }
        if code in hard_code:
            return hard_code[code]

        print(f"Unknown keycode: {code}")
        return -1

    def on_init(self):
        self.setWindowTitle(f"Serial: {self.client.device_name}")
        # self.video_player = VideoStreamPlayer(self.video_widget, self.client.buffer)
        # self.video_player.play()

    def on_frame(self, frame: np.ndarray):
        QApplication.processEvents()
        self.ui.label.update()
        if frame is not None:
            ratio = self.max_width / max(self.client.resolution)
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format_BGR888,
            )
            pix = QPixmap(image)
            pix.setDevicePixelRatio(1 / ratio)
            self.ui.label.setPixmap(pix)
            self.resize(1, 1)

            # set fps and resolution
            if not self.__frame_time_window.full():
                self.__frame_time_window.put_nowait(time.time())
            else:
                last_frame_time = self.__frame_time_window.get_nowait()
                self.__frame_time_window.put_nowait(cur_frame_time := time.time())
                frames = self.__frame_time_window.maxsize
                self.ui.label_fps.setText(
                    f"{frames / (cur_frame_time - last_frame_time):.2f}"
                )

            h, w, _ = frame.shape
            self.ui.label_resolution.setText(f"{w} * {h}")

    def closeEvent(self, _):
        self.serial = None
        self.close_window()
        QApplication.quit()

    def close_window(self):
        self.mouse_recorder.stop_record()

        self.client.stop()
        self.alive = False
        self.mouse_recorder.stop_processor()


def main():
    parser = ArgumentParser(
        description="A simple scrcpy client",
    )
    parser.add_argument(
        "-m",
        "--max_width",
        type=int,
        default=960,
        help="Set max width of the window, default 1280",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=str,
        help="Select device manually (device serial required)",
    )
    parser.add_argument(
        "-s",
        "--max_fps",
        type=int,
        default=60,
        help="Set max fps of the window, default 30, 30 ~ 60 is recommended",
    )
    parser.add_argument(
        "-b",
        "--bitrate",
        type=int,
        default=8_000_000,
        help="Set bitrate of the video, default 8Mbps",
    )
    parser.add_argument("--encoder_name", type=str, help="Encoder name to use")
    args = parser.parse_args()

    if not QApplication.instance():
        app = QApplication([])
    else:
        app = QApplication.instance()
    app.setApplicationName("PyScrcpyClient")
    try:
        m = MainWindow(
            args.max_width, args.device, args.encoder_name, args.max_fps, args.bitrate
        )
    except RuntimeError as e:
        QMessageBox.critical(
            None,
            "ADB Error",
            e.args[0],
            QMessageBox.StandardButton.Ok,
        )
        return
    m.show()
    m.client.start(daemon_thread=True)
    m.client.event_dispatcher_thread_loop()
    m.close_window()
    while s := m.serial:
        m.deleteLater()
        m.destroy(True, True)
        app.processEvents()
        m = MainWindow(args.max_width, s, args.encoder_name, args.max_fps, args.bitrate)
        m.show()
        m.client.start(daemon_thread=True)
        m.client.event_dispatcher_thread_loop()
        m.close_window()
