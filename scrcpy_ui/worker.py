#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import time

import numpy as np
from adbutils import adb
from loguru import logger

from scrcpy import MutiClient


class ThreadWorker(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, serialno, signel=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.stop_flag = False
        self.signel = signel

        self.max_block_frame = 100
        self.time_clean_block_list = 10  # s
        self.list_block_frame_time = []
        self.device = adb.device(serial=serialno)
        self.client = MutiClient(device=self.device, block_frame=False, max_width=640)

    def run(self):
        for frame in self.client.start():
            if self.stop_flag:
                return
            if isinstance(frame, np.ndarray):
                print(frame.shape, "TODO -> Need Server.")
                if self.signel:
                    self.signel.emit(frame)
                pass
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
