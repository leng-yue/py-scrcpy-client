from typing import Optional

import click
from adbutils import adb
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow
from ui_main import Ui_MainWindow

import scrcpy

app = QApplication([])


class MainWindow(QMainWindow):
    def __init__(self, max_width, device):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if device:
            device = adb.device(serial=device)
        elif len(adb.device_list()) > 1:
            devices = adb.device_list()
            print(
                "More than one device founded, please choice an android device to connect:"
            )
            for index, i in enumerate(devices):
                print(f"[{index}] {i.serial}")
            device = devices[int(input("Please type a number here: "))]

        # Setup client
        self.client = scrcpy.Client(max_width=max_width, device=device)
        self.client.add_listener(scrcpy.EVENT_INIT, self.on_init)
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)

        # Bind buttons
        self.ui.button_home.clicked.connect(self.on_click_home)
        self.ui.button_back.clicked.connect(self.on_click_back)
        self.ui.button_stop.clicked.connect(self.on_click_stop)

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)

    def on_click_home(self):
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

    def on_click_back(self):
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

    def on_click_stop(self):
        self.client.stop()

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            self.client.control.touch(evt.position().x(), evt.position().y(), action)

        return handler

    def on_key_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QKeyEvent):
            code = self.map_code(evt.key())
            if code != -1:
                self.client.control.keycode(code, action)

        return handler

    # Mapping numbers, english chars, some other operations
    def map_code(self, code):
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
        print(code)
        return -1

    def on_init(self):
        self.setWindowTitle(f"Serial: {self.client.device_name}")

    def on_frame(self, frame):
        focused_widget = QApplication.focusWidget()
        if focused_widget is not None:
            focused_widget.clearFocus()
        app.processEvents()

        if frame is not None:
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format_BGR888,
            )
            pix = QPixmap(image)
            self.ui.label.setPixmap(pix)
            self.resize(*self.client.resolution)


@click.command(help="A simple scrcpy client")
@click.option(
    "--max_width",
    default=800,
    show_default=True,
    help="Set max width of the window",
)
@click.option(
    "--device",
    help="Select device manually (device serial required)",
)
def main(max_width: int, device: Optional[str]):
    m = MainWindow(max_width, device)
    m.show()
    m.client.start()


if __name__ == "__main__":
    main()
