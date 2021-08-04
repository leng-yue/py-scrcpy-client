from typing import Optional

from scrcpy import Client


class FakeStream:
    def __init__(self, data: list[Optional[bytes]]):
        self.data: list[Optional[bytes]] = data
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
    def __init__(self):
        self.data = [[b"\x00", b"test", b"\x07\x80\x04\x38"], []]

    @staticmethod
    def push(a, b):
        pass

    @staticmethod
    def shell(a, stream=True):
        return FakeStream([])

    def create_connection(self, a, b):
        return FakeStream(self.data.pop(0))


def test_init_listener():
    def init():
        assert client.device_name == "test"
        client.stop()

    client = Client(device=FakeADBDevice())

    client.add_listener("init", init)
    assert client.listeners["init"] == [init]
    client.remove_listener("init", init)
    assert client.listeners["init"] == []

    client.add_listener("init", init)
    client.start()
