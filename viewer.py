import logging
import os
import socket
import struct
import subprocess
import sys
from queue import Queue
from time import sleep

import av

from control import ControlMixin

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class AndroidViewer(ControlMixin):
    video_socket = None
    control_socket = None
    resolution = None

    video_data_queue = Queue()

    def __init__(self, max_width=0, bitrate=8000000, max_fps=30, adb_path='/usr/local/bin/adb',
                 ip='127.0.0.1', port=8081):
        """

        :param max_width: frame width that will be broadcast from android server
        :param bitrate:
        :param max_fps: 0 means not max fps.
        :param ip: android server IP
        :param adb_path: path to ADB
        :param port: android server port
        """
        self.ip = ip
        self.port = port

        self.adb_path = adb_path

        assert self.deploy_server(max_width, bitrate, max_fps)

        self.codec = av.codec.CodecContext.create('h264', 'r')
        self.init_server_connection()

    def receiver(self):
        """
        Read h264 video data from video socket and put it in Queue.
        This method should work in separate thread since it's blocking.
        """
        while True:
            raw_h264 = self.video_socket.recv(0x10000)

            if not raw_h264:
                continue

            self.video_data_queue.put(raw_h264)

    def init_server_connection(self):
        """
        Connect to android server, there will be two sockets, video and control socket.
        This method will set: video_socket, control_socket, resolution variables
        """
        logger.info("Connecting video socket")
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_socket.connect((self.ip, self.port))

        dummy_byte = self.video_socket.recv(1)
        if not len(dummy_byte):
            raise ConnectionError("Did not receive Dummy Byte!")

        logger.info("Connecting control socket")
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.connect((self.ip, self.port))

        device_name = self.video_socket.recv(64).decode("utf-8")

        if not len(device_name):
            raise ConnectionError("Did not receive Device Name!")
        logger.info("Device Name: " + device_name)

        res = self.video_socket.recv(4)
        self.resolution = struct.unpack(">HH", res)
        logger.info("Screen resolution: %s", self.resolution)
        self.video_socket.setblocking(False)

    def deploy_server(self, max_width=1024, bitrate=8000000, max_fps=0):
        try:
            logger.info("Upload JAR...")

            server_root = os.path.abspath(os.path.dirname(__file__))
            server_file_path = server_root + '/scrcpy-server.jar'
            adb_push = subprocess.Popen([self.adb_path, 'push', server_file_path, '/data/local/tmp/'],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=server_root)
            adb_push_comm = ''.join([x.decode("utf-8") for x in adb_push.communicate() if x is not None])

            if "error" in adb_push_comm:
                logger.critical("Is your device/emulator visible to ADB?")
                raise Exception(adb_push_comm)

            logger.info("Running server...")
            subprocess.Popen(
                [self.adb_path, 'shell',
                 'CLASSPATH=/data/local/tmp/scrcpy-server.jar',
                 'app_process', '/', 'com.genymobile.scrcpy.Server 1.12.1 {} {} {} true - false true'.format(
                    max_width, bitrate, max_fps)],
                cwd=server_root)
            sleep(1)

            logger.info("Forward server port...")
            subprocess.Popen(
                [self.adb_path, 'forward', 'tcp:8081', 'localabstract:scrcpy'],
                cwd=server_root).wait()
            sleep(2)
        except FileNotFoundError:
            raise FileNotFoundError("Couldn't find ADB at path ADB_bin: " + str(self.adb_path))

        return True

    def get_next_frames(self):
        """
        Get raw h264 video, parse packets, decode each packet to frames and convert
        each frame to numpy array.
        :return:
        """

        try:
            raw_h264 = self.video_socket.recv(0x10000)
            packets = self.codec.parse(raw_h264)

            if not packets:
                return None

        except socket.error as e:
            return None

        if not packets:
            return None

        result_frames = []

        for packet in packets:
            frames = self.codec.decode(packet)
            for frame in frames:
                result_frames.append(frame.to_ndarray(format="bgr24"))

        return result_frames or None

    def stream_generator(self):
        while True:
            try:
                raw_h264 = self.video_socket.recv(0x10000)
                packets = self.codec.parse(raw_h264)
                for packet in packets:
                    frames = self.codec.decode(packet)
                    for frame in frames:
                        yield frame.to_ndarray(format="bgr24")
            except:
                yield None
