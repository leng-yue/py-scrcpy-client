import os
import socket
import struct
import subprocess
from time import sleep
from typing import Any, Callable, Generator, Optional

import cv2
import numpy as np
from av.codec import CodecContext

from .control import ControlSender


class Client:
    def __init__(
        self,
        max_width=0,
        bitrate=8000000,
        max_fps=0,
        adb_path="/usr/local/bin/adb",
        ip="127.0.0.1",
        port=8081,
        flip=False,
        block_frame=False,
    ):
        """
        Create a scrcpy client, this client won't be started until you call the start function
        :param max_width: frame width that will be broadcast from android server
        :param bitrate: bitrate
        :param max_fps: 0 means not max fps. supported after android 10
        :param adb_path: adb path
        :param ip: android server IP
        :param port: android server port
        :param flip: flip the video
        :param block_frame: only return nonempty frames, may block cv2 render thread
        """

        self.ip = ip
        self.port = port
        self.listeners = dict(frame=[], init=[])
        self.last_frame = None
        self.video_socket = None
        self.control_socket = None
        self.resolution = None
        self.adb_path = adb_path
        self.flip = flip
        self.device_name = None
        self.control = ControlSender(self)
        self.max_width = max_width
        self.bitrate = bitrate
        self.max_fps = max_fps
        self.block_frame = block_frame

    def init_server_connection(self):
        """
        Connect to android server, there will be two sockets, video and control socket.
        This method will set: video_socket, control_socket, resolution variables
        """

        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_socket.connect((self.ip, self.port))

        dummy_byte = self.video_socket.recv(1)
        if not len(dummy_byte):
            raise ConnectionError("Did not receive Dummy Byte!")

        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.connect((self.ip, self.port))

        self.device_name = self.video_socket.recv(64).decode("utf-8")

        if not len(self.device_name):
            raise ConnectionError("Did not receive Device Name!")

        res = self.video_socket.recv(4)
        self.resolution = struct.unpack(">HH", res)
        self.video_socket.setblocking(False)

    def deploy_server(self):
        """
        Deploy server to android device
        """

        if not os.path.exists(self.adb_path):
            raise FileNotFoundError(
                "Couldn't find ADB at path ADB_bin: " + str(self.adb_path)
            )

        server_root = os.path.abspath(os.path.dirname(__file__))
        server_file_path = server_root + "/scrcpy-server.jar"
        adb_push = subprocess.Popen(
            [self.adb_path, "push", server_file_path, "/data/local/tmp/"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=server_root,
        )
        adb_push_comm = "".join(
            [x.decode("utf-8") for x in adb_push.communicate() if x is not None]
        )

        if "error" in adb_push_comm:
            raise ConnectionError("Is your device/emulator visible to ADB?")

        subprocess.Popen(
            [
                self.adb_path,
                "shell",
                "CLASSPATH=/data/local/tmp/scrcpy-server.jar",
                "app_process",
                "/",
                "com.genymobile.scrcpy.Server 1.12.1 {} {} {} true - false true".format(
                    self.max_width, self.bitrate, self.max_fps
                ),
            ],
            cwd=server_root,
        )
        sleep(1)

        subprocess.Popen(
            [self.adb_path, "forward", f"tcp:{self.port}", "localabstract:scrcpy"],
            cwd=server_root,
        ).wait()
        sleep(1)

    def start(self) -> None:
        """
        Start listening video stream
        """
        self.deploy_server()
        self.init_server_connection()
        self.__send_to_listeners("init")

        for i in self.__stream_generator():
            if i is not None:
                self.last_frame = i
                self.resolution = (i.shape[1], i.shape[0])
            self.__send_to_listeners("frame", i)

    def __stream_generator(self) -> Generator[Optional[np.ndarray], None, None]:
        """
        Parsing h264 stream to frames
        :return: frames
        """
        codec = CodecContext.create("h264", "r")

        while True:
            try:
                raw_h264 = self.video_socket.recv(0x10000)
                packets = codec.parse(raw_h264)
                for packet in packets:
                    frames = codec.decode(packet)
                    for frame in frames:
                        frame = frame.to_ndarray(format="bgr24")
                        if self.flip:
                            frame = cv2.flip(frame, 1)
                        yield frame
            except BlockingIOError:
                if not self.block_frame:
                    yield None

    def add_listener(self, cls: str, listener: Callable[..., Any]) -> None:
        """
        Add a video listener
        :param cls: Listener category, support: init, frame
        :param listener: A function to receive frame np.ndarray
        """
        self.listeners[cls].append(listener)

    def remove_listener(self, cls: str, listener: Callable[..., Any]) -> None:
        """
        Remove a video listener
        :param cls: Listener category, support: init, frame
        :param listener: A function to receive frame np.ndarray
        """
        self.listeners[cls].remove(listener)

    def __send_to_listeners(self, cls: str, *args, **kwargs):
        for fun in self.listeners[cls]:
            fun(*args, **kwargs)
