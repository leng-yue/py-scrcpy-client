#!/usr/bin/python
# -*- coding: UTF-8 -*-
import threading
import time

from adbutils import adb

from scrcpy import MutiClient


class ThreadWorker(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, serialno):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.stop_flag = False

        self.device = adb.device(serial=serialno)
        self.client = MutiClient(device=self.device, bitrate=1000000000)

    def run(self):
        for frame in self.client.start():
            if self.stop_flag:
                return
            print(".")

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
