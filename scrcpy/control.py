import struct
from time import sleep

from scrcpy import const


class ControlSender:
    def __init__(self, parent, move_step_length=5, move_steps_delay=0.005):
        self.parent = parent
        self.move_step_length = move_step_length
        self.move_steps_delay = move_steps_delay

    def keycode(self, keycode, action=const.ACTION_DOWN):
        self.parent.control_socket.send(struct.pack(">BBII", 0, action, keycode, 0))

    def touch(self, x, y, action=const.ACTION_DOWN):
        b = struct.pack(">BB", 2, action)
        b += b"\xff\xff\xff\xff\xff\xff\xff\xff"
        b += struct.pack(
            ">IIhh",
            int(x),
            int(y),
            int(self.parent.resolution[0]),
            int(self.parent.resolution[1]),
        )
        b += b"\xff\xff"  # Pressure
        b += b"\x00\x00\x00\x01"  # Event button primary
        self.parent.control_socket.send(b)

    def swipe(self, start_x, start_y, end_x, end_y):
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
                next_x -= self.move_step_length
                if next_x < end_x:
                    next_x = end_x
            else:
                next_x += self.move_step_length
                if next_x > end_x:
                    next_x = end_x

            if decrease_y:
                next_y -= self.move_step_length
                if next_y < end_y:
                    next_y = end_y
            else:
                next_y += self.move_step_length
                if next_y > end_y:
                    next_y = end_y

            self.touch(next_x, next_y, const.ACTION_MOVE)

            if next_x == end_x and next_y == end_y:
                self.touch(next_x, next_y, const.ACTION_UP)
                break
            sleep(self.move_steps_delay)
