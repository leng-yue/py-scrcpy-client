import pathlib
import pickle

import pytest
from adbutils import AdbError

from scrcpy import Client
from tests.utils import FakeStream


class Sync:
    @staticmethod
    def push(a, b):
        pass


class FakeADBDevice:

    sync = Sync()

    def __init__(self, data, wait=0):
        self.data = data
        self.__wait = wait

    @staticmethod
    def shell(a, stream=True):
        return FakeStream([b"\x00" * 128])

    def create_connection(self, a, b):
        if self.__wait > 0:
            self.__wait -= 1
            raise AdbError()

        return FakeStream(self.data.pop(0))


def test_connection():
    client = Client(
        device=FakeADBDevice([[b"\x00", b"test", b"\x07\x80\x04\x38"], []], wait=3)
    )
    client.start(threaded=True)
    client.stop()

    with pytest.raises(ConnectionError):
        client = Client(
            device=FakeADBDevice(
                [[b"\x00", b"test", b"\x07\x80\x04\x38"], []], wait=1000
            ),
            connection_timeout=1000,
        )
        client.start(threaded=True)
        client.stop()

    # No Dummy Bytes Error
    with pytest.raises(ConnectionError) as e:
        client = Client(
            device=FakeADBDevice([[b"\x01", b"test", b"\x07\x80\x04\x38"], []])
        )
        client.start(threaded=True)
        client.stop()
    assert "Dummy Byte" in str(e.value)

    # No Device Name Error
    with pytest.raises(ConnectionError) as e:
        client = Client(device=FakeADBDevice([[b"\x00", b"", b"\x07\x80\x04\x38"], []]))
        client.start(threaded=True)
        client.stop()
    assert "Device Name" in str(e.value)


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
    data = [
        [b"\x00", b"test", b"\x07\x80\x04\x38", None] + video_data + [b"OSError"],
        [],
    ]
    frames = []

    # Create client
    client = Client(device=FakeADBDevice(data), flip=True)
    client.add_listener("frame", on_frame)
    with pytest.raises(OSError):
        client.start()

    # Wait frames
    assert frames[0] is None
    assert frames[1].shape == (800, 368, 3)
    assert frames[2].shape == (800, 368, 3)
