import datetime
import json
import os
import queue
from typing import Optional

import cv2
from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread, QPoint
from numpy.core._multiarray_umath import ndarray

import scrcpy
from scrcpy_ui.logger import Logger


class MouseRecord(QObject):
    def __init__(self, pos: QPoint, frame: ndarray):
        super().__init__()
        self.pos = pos
        self.frame = frame


class MouseRecordProcessor(QThread):
    onRecordSaved = QtCore.Signal(str, int, int)

    def __init__(self, queue: queue.Queue[Optional[MouseRecord]], save_dir: str):
        super().__init__()
        self.queue = queue
        self.count = 0
        self.save_dir = save_dir  # 保存目录

    def run(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        print("MouseRecordProcessor started")
        while True:
            record: MouseRecord = self.queue.get()
            if record is None:
                break
            self.count += 1
            record_name = f"mouse_record_{self.count}"
            pos, frame = record.pos, record.frame
            # 在frame的pos处绘制一个长宽20pixel,厚度为2pixel的红色十字
            # 1. 获取frame的shape
            # 2. 计算十字的起始点和终止点
            # 3. 绘制十字
            # 4. 保存frame
            height, width, _ = frame.shape

            # 绘制一个竖着的线
            cv2.line(frame, (pos.x(), 0), (pos.x(), height), (0, 0, 255), 2)
            # 绘制一个横着的线
            cv2.line(frame, (0, pos.y()), (width, pos.y()), (0, 0, 255), 2)

            os.makedirs(self.save_dir, exist_ok=True)
            # 保存frame
            cv2.imwrite(f"{self.save_dir}/{record_name}.png", frame)
            # 保存记录
            with open(f"{self.save_dir}/mouse_records.txt", "a", encoding="utf-8") as f:
                json.dump(
                    {
                        "name": record_name,
                        "pos": [int(pos.x()), int(pos.y())],
                        "window_size": [width, height],
                        "relative_pos": [
                            int(100 * pos.x() / width),
                            int(100 * pos.y() / height),
                        ],
                        "frame": f"{record_name}.png",
                        "time": datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S.%f"
                        )[:-3],
                    },
                    f,
                    ensure_ascii=False,
                )

            self.onRecordSaved.emit(record_name, pos.x(), pos.y())
            record.deleteLater()  # 释放内存
        print("MouseRecordProcessor exited")


class MouseRecorder(QObject):
    def __init__(self, client: scrcpy.Client, save_dir: Optional[str] = None):
        super().__init__()
        self.__mouse_records = queue.Queue()
        self.__is_recording = False
        self.client = client
        self.save_dir = save_dir or "mouse_records"
        self.processor = MouseRecordProcessor(
            self.__mouse_records, save_dir=self.save_dir
        )
        self.logger = Logger.get_logger()

        self.processor.started.connect(self.on_process_started)
        self.processor.onRecordSaved.connect(self.on_processor_saved)
        self.processor.start()

    def on_mouse_released(self, pos: QPoint):
        if self.__is_recording:
            frame: ndarray = self.client.last_frame
            if frame is None:
                return
            self.__mouse_records.put(MouseRecord(pos, frame.copy()))

    def on_process_started(self):
        self.logger.debug(msg="thread started", sender=self.processor)

    def on_processor_saved(self, name: str, x: int, y: int):
        self.logger.success(
            msg=f"Mouse Click Event Recorded: {name=} ({x=}, {y=})",
            sender=self.processor,
        )

    def start_record(self):
        self.__is_recording = True

    def stop_record(self):
        self.__is_recording = False

    def stop_processor(self):
        self.__mouse_records.put(None)
        self.processor.wait(deadline=1000)
        self.processor.terminate()

    @property
    def is_recording(self):
        return self.__is_recording
