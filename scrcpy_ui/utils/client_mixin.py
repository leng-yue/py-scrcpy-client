from PySide6.QtCore import Signal, QObject

from av.codec import CodecContext
from av.error import InvalidDataError
import cv2
import time

from scrcpy import Client


class QScrcpyClient(QObject, Client):
    onFrame = Signal(object)  # stub
    onDisconnect = Signal(object)  # stub

    def __stream_loop_in_thread(self) -> None:
        """
        Core loop for video parsing
        """
        codec = CodecContext.create("h264", "r")
        while self.alive:
            try:
                raw_h264 = self.__video_socket.recv(0x10000)
                self.buffer.put(raw_h264)
                if raw_h264 == b"":
                    raise ConnectionError("Video stream is disconnected")
                packets = codec.parse(raw_h264)
                for packet in packets:
                    frames = codec.decode(packet)
                    for frame in frames:
                        frame = frame.to_ndarray(format="bgr24")
                        if self.flip:
                            frame = cv2.flip(frame, 1)
                        self.last_frame = frame
                        self.resolution = (frame.shape[1], frame.shape[0])
                        self.onFrame.emit(frame)
            except (BlockingIOError, InvalidDataError):
                time.sleep(0.01)
                if not self.block_frame:
                    self.onFrame.emit(None)
            except (ConnectionError, OSError) as e:  # Socket Closed
                if self.alive:
                    self.onDisconnect.emit(None)
                    self.stop()
                    raise e
