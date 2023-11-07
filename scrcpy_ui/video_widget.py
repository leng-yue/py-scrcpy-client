import queue

from PySide6 import QtCore
from PySide6.QtCore import Slot, QIODevice
from PySide6.QtGui import QImage
from PySide6.QtMultimedia import QMediaPlayer, QVideoSink, QVideoFrame
from PySide6.QtMultimediaWidgets import QVideoWidget


class SimpleQueueWrapper(QIODevice):
    def __init__(self, queue: queue.SimpleQueue[bytes]):
        super().__init__()
        self.queue = queue

    def read(self, maxlen: int) -> QtCore.QByteArray:
        print("read")
        try:
            return QtCore.QByteArray(self.queue.get_nowait())
        except queue.Empty:
            return QtCore.QByteArray()

    def isSequential(self) -> bool:
        return True

    def readData(self, maxlen: int) -> object:
        print("readData")
        if maxlen == 0:
            return QtCore.QByteArray()
        rv: QtCore.QByteArray = self.read(maxlen)
        if rv:
            return rv.data()
        else:
            return 0

    def bytesAvailable(self) -> int:
        if self.queue.empty():
            return 0
        else:
            return 0x10000

    def writeData(self, data: bytes, len: int) -> int:
        return -1


class VideoStreamPlayer(QMediaPlayer):
    onScreenShot = QtCore.Signal(QImage, QtCore.QSize)

    def __init__(self, video_widget: QVideoWidget, device: QIODevice, parent=None):
        super().__init__(parent)
        self.device = device

        # widget ref
        self.video_widget = video_widget

        # self settings
        self.setVideoOutput(video_widget)
        self.setSourceDevice(self.device)
        self.screen_shot_surface = QVideoSink()

        # bind signal
        self.errorOccurred.connect(lambda error: print(error))

    def async_screen_shot(self):
        # 1.连接sink
        self.setVideoOutput(self.screen_shot_surface)
        # 2.连接信号
        self.screen_shot_surface.videoFrameChanged.connect(self.on_frame_available)

    @Slot(QVideoFrame)
    def on_frame_available(self, frame: QVideoFrame):
        # 1.获取frame
        # 2.断开信号
        # 3.恢复sink
        self.screen_shot_surface.videoFrameChanged.disconnect(self.on_frame_available)
        self.setVideoOutput(self.video_widget)
        self.onScreenShot.emit(frame.toImage(), frame.size())
