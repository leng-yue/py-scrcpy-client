#!/usr/bin/python
# -*- coding: UTF-8 -*-
import socket
import threading
import time

import numpy as np
from adbutils import adb
from loguru import logger
from PySide6.QtCore import Signal

from scrcpy import MutiClient

from .schemas import ServerInfo


class ThreadWorker(threading.Thread):  # 继承父类threading.Thread
    def __init__(
        self, threadID, serialno, signal: Signal = None, serverinfo: ServerInfo = None
    ):
        """
        signal  通过Qt Signel slot机制进行桌面端手机画面显示
        serverinfo 将手机画面传输到服务端处理
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.stop_flag = False
        self.signal = signal
        self.serverinfo = None
        if serverinfo:
            self.serverinfo = self.get_server(serverinfo)
        self.max_block_frame = 100
        self.time_clean_block_list = 10  # s
        self.list_block_frame_time = []
        self.device = adb.device(serial=serialno)
        self.client = MutiClient(device=self.device, block_frame=False, max_width=640)

    def get_server(self, serverinfo: ServerInfo):
        serverinfo.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return serverinfo

    def encode_content(self, data):
        if isinstance(data, str):
            return data.encode()
        return

    def run(self):
        for frame in self.client.start():
            if self.stop_flag:
                return
            if isinstance(frame, np.ndarray):
                if self.signal:
                    self.signal.emit(frame)
                else:
                    self.serverinfo.server.sendto(
                        self.encode_content("hello. Wakeup and goto work!"),
                        (self.serverinfo.host, self.serverinfo.port),
                    )
                    print(f"> send udp 2 {self.serverinfo.host}:{self.serverinfo.port}")
                    rst = self.serverinfo.server.recv(100)
                    print(f"< recv udp recall !!!!! {rst}")
            else:
                now = time.time()
                if not self.list_block_frame_time:
                    self.list_block_frame_time.append(now)
                elif len(self.list_block_frame_time) >= self.max_block_frame:
                    logger.warning(
                        f"max_block_frame out size: {self.list_block_frame_time}"
                    )
                    self.list_block_frame_time = []
                elif now - self.list_block_frame_time[-1] >= self.time_clean_block_list:
                    self.list_block_frame_time = []
                elif (
                    now - self.list_block_frame_time[-1]
                    < self.time_clean_block_list / 10
                ):
                    self.list_block_frame_time.append(now)

    def stop(self):
        if self.serverinfo:
            self.serverinfo.server = None
        self.stop_flag = True


if __name__ == "__main__":
    # 创建新线程
    thread1 = ThreadWorker(1, "Thread-1")
    thread2 = ThreadWorker(2, "Thread-2")

    # 开启线程
    thread1.start()
    thread2.start()
    time.sleep(1)
    thread1.stop_flag = True
    thread2.stop_flag = True
