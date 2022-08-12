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

from .schemas import RspInfo, ServerInfo
from .utils import StructPack, imencode


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
        self.serverinfo = serverinfo
        self.max_block_frame = 100
        self.time_add_block_list = 2  # s
        self.list_block_frame_time = []
        self.serialno = serialno
        self.device = adb.device(serial=serialno)
        self.client = MutiClient(device=self.device, block_frame=False, max_width=640)

    def get_server(self, serverinfo: ServerInfo):
        serverinfo.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverinfo.server.setblocking(0)
        return serverinfo

    def http_send(self, img):
        # TODO 在这里实现调用AI服务
        bimg = imencode(img)
        rst = None
        return rst

    def udp_split_send(self, img):
        # TODO 在这里实现调用AI服务
        bimg = imencode(img)
        len_img = len(bimg)

        len_fhead, fhead = StructPack.struct_pack(
            len_data=len_img, serialno=self.serialno
        )
        if not len_fhead or self.serverinfo.server is None:
            logger.error("udp send error: pack error")
            return
        self.serverinfo.server.sendto(
            fhead, (self.serverinfo.host, self.serverinfo.port)
        )

        for i in range(len(bimg) // (1024 - len_fhead) + 1):
            if (1024 - len_fhead) * (i + 1) > len_img:
                segment = bimg[(1024 - len_fhead) * i :]
                self.serverinfo.server.sendto(
                    (fhead + segment),
                    (self.serverinfo.host, self.serverinfo.port),
                )
            else:
                segment = bimg[(1024 - len_fhead) * i : (1024 - len_fhead) * (i + 1)]
                self.serverinfo.server.sendto(
                    (fhead + segment),
                    (self.serverinfo.host, self.serverinfo.port),
                )
        print(f"> send udp 2 {self.serverinfo.host}:{self.serverinfo.port}")

    def get_udp_recv(self):
        try:
            resp = self.serverinfo.server.recv(100)
            return RspInfo.decode(resp)
        except BlockingIOError:
            return None

    def run(self):
        if self.serverinfo:
            self.serverinfo = self.get_server(self.serverinfo)
        for frame in self.client.start():
            if self.stop_flag:
                return
            if isinstance(frame, np.ndarray):
                if self.signal:
                    self.signal.emit(frame)
                else:
                    self.udp_split_send(img=frame)
                    rst = self.get_udp_recv()
                    if rst:
                        print(f"< recv{self.serialno} udp recall !!!!! {rst}")
                    else:
                        print("udp not reponse!")
            else:
                now = time.time()
                if not self.list_block_frame_time:
                    self.list_block_frame_time.append(now)
                elif len(self.list_block_frame_time) >= self.max_block_frame:
                    logger.debug(
                        f"max_block_frame out size: {self.list_block_frame_time}"
                    )
                    self.list_block_frame_time = []
                elif (
                    now - self.list_block_frame_time[-1]
                    >= self.time_add_block_list * 10
                ):
                    self.list_block_frame_time = []
                elif now - self.list_block_frame_time[-1] > self.time_add_block_list:
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
