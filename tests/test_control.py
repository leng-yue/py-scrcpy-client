import scrcpy
from scrcpy.control import ControlSender


class MockParent:
    control_socket = None
    resolution = (1920, 1080)


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
        b"\x04" + b"\x00"  # TYPE_BACK_OR_SCREEN_ON  # ACTION_DOWN
    )


def test_swipe():
    control.swipe(100, 200, 300, 400)
    control.swipe(100, 200, 2000, 2000)
    control.swipe(300, 400, 100, 200)
    control.swipe(2000, 2000, 100, 200)
