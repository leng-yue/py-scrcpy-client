class FakeStream:
    def __init__(self, data=None):
        if data is None:
            data = []
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
        if val == b"OSError":
            raise OSError()
        return val

    def read(self, a):
        return self.recv(a)

    def check_okay(self):
        return

    @staticmethod
    def setblocking(a):
        pass

    def close(self):
        self.die = True

    def send(self, x):
        pass
