import pathlib
import pickle
from typing import Optional

from scrcpy import Client


class FakeStream:
    def __init__(self, data):
        self.data = data
        self.die = False

    def recv(self, a):
        if self.die:
            raise OSError()
        if len(self.data) == 0:
            raise BlockingIOError()
        val = self.data.pop(0)
        if val is None:
            raise BlockingIOError()
        return val

    @staticmethod
    def setblocking(a):
        pass

    def close(self):
        self.die = True


class FakeADBDevice:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def push(a, b):
        pass

    @staticmethod
    def shell(a, stream=True):
        return FakeStream([])

    def create_connection(self, a, b):
        return FakeStream(self.data.pop(0))


def test_init_listener():
    def on_init():
        assert client.device_name == "test"
        client.stop()

    client = Client(device=FakeADBDevice([[b"\x00", b"test", b"\x07\x80\x04\x38"], []]))

    client.add_listener("init", on_init)
    assert client.listeners["init"] == [on_init]
    client.remove_listener("init", on_init)
    assert client.listeners["init"] == []

    client.add_listener("init", on_init)
    client.start(threaded=True)


def test_parse_video():
    def on_frame(frame):
        frames.append(frame)
        if len(frames) == 5:
            client.stop()

    # Load test data
    video_data = pickle.load(
        (pathlib.Path(__file__).parent / "test_video_data.pkl").resolve().open("rb")
    )
    data = [[b"\x00", b"test", b"\x07\x80\x04\x38", None] + video_data, []]
    frames = []

    # Create client
    client = Client(device=FakeADBDevice(data), flip=True)
    client.add_listener("frame", on_frame)
    client.start()

    # Wait frames
    assert frames[0] is None
    assert frames[1].shape == (800, 368, 3)
    assert frames[2].shape == (800, 368, 3)
