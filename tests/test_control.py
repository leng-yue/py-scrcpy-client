import threading

import scrcpy
from scrcpy.control import ControlSender
from tests.utils import FakeStream


class MockParent:
    class FakeSocket:
        def send(self, data):
            pass

    resolution = (1920, 1080)

    def __init__(self):
        self.control_socket_lock = threading.Lock()
        self.control_socket = FakeStream()


control = ControlSender(MockParent())


def test_control_keycode():
    assert control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN, 1) == (
        b"\x00"  # TYPE_INJECT_KEYCODE
        + b"\x00"  # ACTION_DOWN
        + b"\x00\x00\x00\x03"  # KEYCODE_HOME
        + b"\x00\x00\x00\x01"  # Repeat = 1
        + b"\x00\x00\x00\x00"  # MetaState = 0
    )


def test_control_touch():
    assert control.touch(100, 200, scrcpy.ACTION_DOWN) == (
        b"\x02"  # TYPE_INJECT_TOUCH_EVENT
        + b"\x00"  # ACTION_DOWN
        + b"\xff\xff\xff\xff\xff\xff\xff\xff"  # Virtual touch id
        + b"\x00\x00\x00\x64"  # X: 100
        + b"\x00\x00\x00\xc8"  # Y: 200
        + b"\x07\x80\x04\x38"  # Resolution: (1920, 1080)
        + b"\xff\xff"  # Pressure: 100%
        + b"\x00\x00\x00\x01"  # Primary button
    )


def test_control_text():
    text = "hello, world"
    assert control.text(text) == (
        b"\x01"  # TYPE_INJECT_TEXT
        + b"\x00\x00\x00\x0c"  # Length: 12
        + text.encode("utf-8")
    )


def test_control_scroll():
    assert control.scroll(100, 200, 100, 200) == (
        b"\x03"  # TYPE_INJECT_SCROLL_EVENT
        + b"\x00\x00\x00\x64"  # X: 100
        + b"\x00\x00\x00\xc8"  # Y: 200
        + b"\x07\x80\x04\x38"  # Resolution: (1920, 1080)
        + b"\x00\x00\x00\x64"  # H: 100
        + b"\x00\x00\x00\xc8"  # V: 200
    )


def test_back_or_turn_screen_on():
    assert control.back_or_turn_screen_on() == (
        b"\x04" + b"\x00"  # TYPE_BACK_OR_SCREEN_ON, ACTION_DOWN
    )


def test_panels():
    assert control.expand_notification_panel() == b"\x05"
    assert control.expand_settings_panel() == b"\x06"
    assert control.collapse_panels() == b"\x07"


def test_get_clipboard():
    class MockClipboardParent:
        class MockSocket:
            @staticmethod
            def setblocking(_):
                pass

            @staticmethod
            def send(_):
                pass

            @staticmethod
            def recv(b):
                if b == 1024:
                    raise BlockingIOError()
                elif b == 1:
                    return b"\x00"
                elif b == 4:
                    return b"\x00\x00\x00\x05"
                return b"test0"

        control_socket = MockSocket()
        control_socket_lock = threading.Lock()

    assert ControlSender(MockClipboardParent()).get_clipboard() == "test0"


def test_set_clipboard():
    text = "hello, world"
    assert control.set_clipboard(text, False) == (
        b"\x09"  # TYPE_SET_CLIPBOARD
        + b"\x00"  # Paste: false
        + b"\x00\x00\x00\x0c"  # Length: 12
        + text.encode("utf-8")
    )
    assert control.set_clipboard(text, True) == (
        b"\x09"  # TYPE_SET_CLIPBOARD
        + b"\x01"  # Paste: true
        + b"\x00\x00\x00\x0c"  # Length: 12
        + text.encode("utf-8")
    )


def test_set_screen_power_mode():
    assert control.set_screen_power_mode(scrcpy.POWER_MODE_NORMAL) == (
        b"\x0a" + b"\x02"  # TYPE_SET_SCREEN_POWER_MODE, POWER_MODE_NORMAL
    )


def rotate_device():
    assert control.rotate_device() == b"\x0b"  # TYPE_ROTATE_DEVICE


def test_swipe():
    control.swipe(100, 200, 300, 400)
    control.swipe(100, 200, 2000, 2000)
    control.swipe(300, 400, 100, 200)
    control.swipe(2000, 2000, 100, 200)
    control.swipe(2000, 2000, -100, -200)
    control.swipe(100, 200, 2010, 2010, move_step_length=100)
