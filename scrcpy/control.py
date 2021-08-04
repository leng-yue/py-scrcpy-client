import functools
import struct
from time import sleep

from scrcpy import const


def inject(control_type: int):
    """
    Inject control code, with this inject, we will be able to do unit test
    :param control_type:
    :return:
    """

    def wrapper(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            package = struct.pack(">B", control_type) + f(*args, **kwargs)
            if args[0].parent.control_socket is not None:
                args[0].parent.control_socket.send(package)
            return package

        return inner

    return wrapper


class ControlSender:
    def __init__(self, parent):
        self.parent = parent

    @inject(const.TYPE_INJECT_KEYCODE)
    def keycode(
        self, keycode: int, action: int = const.ACTION_DOWN, repeat: int = 0
    ) -> bytes:
        """
        Send keycode to device
        :param keycode: const.KEYCODE_*
        :param action: ACTION_DOWN | ACTION_UP
        :param repeat: repeat count
        """
        return struct.pack(">Biii", action, keycode, repeat, 0)

    @inject(const.TYPE_INJECT_TOUCH_EVENT)
    def touch(
        self, x: int, y: int, action: int = const.ACTION_DOWN, touch_id: int = -1
    ) -> bytes:
        """
        Touch screen
        :param x: Position x
        :param y: Position y
        :param action: ACTION_DOWN | ACTION_UP | ACTION_MOVE
        :param touch_id: Default using virtual id -1, you can specify it to emulate multi finger touch
        """
        x, y = max(x, 0), max(y, 0)
        return struct.pack(
            ">BqiiHHHi",
            action,
            touch_id,
            int(x),
            int(y),
            int(self.parent.resolution[0]),
            int(self.parent.resolution[1]),
            0xFFFF,
            1,
        )

    @inject(const.TYPE_INJECT_TEXT)
    def text(self, text: str) -> bytes:
        """
        Send text to device
        :param text:
        """

        buffer = text.encode("utf-8")
        return struct.pack(">i", len(buffer)) + buffer

    @inject(const.TYPE_INJECT_SCROLL_EVENT)
    def scroll(self, x: int, y: int, h: int, v: int) -> bytes:
        """
        Scroll screen
        :param x:
        :param y:
        :param h: horizontal movement
        :param v: vertical movement
        """

        x, y = max(x, 0), max(y, 0)
        return struct.pack(
            ">iiHHii",
            int(x),
            int(y),
            int(self.parent.resolution[0]),
            int(self.parent.resolution[1]),
            int(h),
            int(v),
        )

    @inject(const.TYPE_BACK_OR_SCREEN_ON)
    def back_or_turn_screen_on(self, action: int = const.ACTION_DOWN) -> bytes:
        """
        If the screen is off, it is turned on only on ACTION_DOWN
        :param action: ACTION_DOWN | ACTION_UP
        """
        return struct.pack(">B", action)

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        move_step_length: int = 5,
        move_steps_delay: float = 0.005,
    ) -> None:
        self.touch(start_x, start_y, const.ACTION_DOWN)
        next_x = start_x
        next_y = start_y

        if end_x > self.parent.resolution[0]:
            end_x = self.parent.resolution[0]

        if end_y > self.parent.resolution[1]:
            end_y = self.parent.resolution[1]

        decrease_x = True if start_x > end_x else False
        decrease_y = True if start_y > end_y else False
        while True:
            if decrease_x:
                next_x -= move_step_length
                if next_x < end_x:
                    next_x = end_x
            else:
                next_x += move_step_length
                if next_x > end_x:
                    next_x = end_x

            if decrease_y:
                next_y -= move_step_length
                if next_y < end_y:
                    next_y = end_y
            else:
                next_y += move_step_length
                if next_y > end_y:
                    next_y = end_y

            self.touch(next_x, next_y, const.ACTION_MOVE)

            if next_x == end_x and next_y == end_y:
                self.touch(next_x, next_y, const.ACTION_UP)
                break
            sleep(move_steps_delay)
