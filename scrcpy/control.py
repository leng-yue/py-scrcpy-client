import struct
from time import sleep

from scrcpy import const


class ControlSender:
    def __init__(self, parent):
        self.parent = parent

    def keycode(self, keycode: int, action: int = const.ACTION_DOWN):
        package = struct.pack(
            ">BBIII", const.TYPE_INJECT_KEYCODE, action, keycode, 0, 0
        )
        self.parent.control_socket.send(package)

    def touch(self, x: int, y: int, action: int = const.ACTION_DOWN):
        x, y = max(x, 0), max(y, 0)
        package = struct.pack(
            ">BBQIIHHHI",
            const.TYPE_INJECT_TOUCH_EVENT,
            action,
            0xFFFFFFFFFFFFFFFF,
            int(x),
            int(y),
            int(self.parent.resolution[0]),
            int(self.parent.resolution[1]),
            0xFFFF,
            1,
        )
        self.parent.control_socket.send(package)

    def text(self, string: str):
        buffer = string.encode("utf-8")
        package = struct.pack(">Bi", const.TYPE_INJECT_TEXT, len(buffer)) + buffer
        self.parent.control_socket.send(package)

    def swipe(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        move_step_length: int = 5,
        move_steps_delay: float = 0.005,
    ):
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
