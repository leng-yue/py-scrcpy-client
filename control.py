import struct
from time import sleep


class ControlMixin:
    ACTION_MOVE = 2
    ACTION_DOWN = 0
    ACTION_UP = 1

    move_step_length = 5  # Move by 5 pixels in one iteration
    move_steps_delay = 0.005  # Delay between each move step

    # Define in base class
    resolution = None
    control_socket = None

    def _build_touch_message(self, x, y, action):
        b = struct.pack('>BB', 2, action)
        b += b'\xff\xff\xff\xff\xff\xff\xff\xff'
        b += struct.pack('>IIhh', int(x), int(y), int(self.resolution[0]), int(self.resolution[1]))
        b += b'\xff\xff'  # Pressure
        b += b'\x00\x00\x00\x01'  # Event button primary
        return bytes(b)

    def send_key_event(self, keycode, action):
        self.control_socket.send(struct.pack('>BBII', 0, action, keycode, 0))

    def swipe(self, start_x, start_y, end_x, end_y):
        self.control_socket.send(self._build_touch_message(x=start_x, y=start_y, action=self.ACTION_DOWN))
        next_x = start_x
        next_y = start_y

        if end_x > self.resolution[0]:
            end_x = self.resolution[0]

        if end_y > self.resolution[1]:
            end_y = self.resolution[1]

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

            self.control_socket.send(self._build_touch_message(x=next_x, y=next_y, action=self.ACTION_MOVE))

            if next_x == end_x and next_y == end_y:
                self.control_socket.send(self._build_touch_message(x=next_x, y=next_y, action=self.ACTION_UP))
                break
            sleep(self.move_steps_delay)

    def send_event(self, x, y, action=ACTION_DOWN):
        self.control_socket.send(self._build_touch_message(x=x, y=y, action=action))
