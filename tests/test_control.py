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
