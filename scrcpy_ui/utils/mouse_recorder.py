import json
import queue
from typing import Optional

import cv2
from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread, QPoint
from PySide6.QtGui import QMouseEvent
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

    def __init__(self, queue: queue.Queue[Optional[MouseRecord]]):
        super().__init__()
        self.queue = queue
        self.count = 0

    def run(self) -> None:
        def get_safe_range(pos: QPoint, width: int, height: int, length: int):
            x, y = pos.x(), pos.y()
            x1, y1 = x - length, y - length
            x2, y2 = x + length, y + length
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            if x2 > width:
                x2 = width
            if y2 > height:
                y2 = height
            return x1, y1, x2, y2

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
            height, width = frame.shape
            x1, y1, x2, y2 = get_safe_range(pos, width, height, 20)
            frame = cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            frame = cv2.line(frame, (x1, y2), (x2, y1), (0, 0, 255), 2)
            # 保存frame
            cv2.imwrite(f"{record_name}.png", frame)
            # 保存记录
            with open("mouse_records.txt", "a", encoding='utf-8') as f:
                record_entry = json.dumps({
                    "pos": [pos.x(), pos.y()],
                    "window_size": [width, height],
                    "relative_pos": [f"{100 * pos.x() / width:.0f}", f'{100 * pos.y() / height:.0f}'],
                    "frame": f"{record_name}.png"
                }, indent=4, ensure_ascii=False)
                f.write(f'{record_name} = {record_entry}\n')

            self.onRecordSaved.emit(record_name, pos.x(), pos.y())
            record.deleteLater()  # 释放内存
        print("MouseRecordProcessor exited")


class MouseRecorder(QObject):
    def __init__(self, client: scrcpy.Client):
        super().__init__()
        self.__mouse_records = queue.Queue()
        self.__is_recording = False
        self.client = client
        self.processor = MouseRecordProcessor(self.__mouse_records)
        self.logger = Logger.get_logger()

        self.processor.started.connect(self.on_process_started)
        self.processor.onRecordSaved.connect(self.on_processor_saved)
        self.processor.start()

    def on_mouse_released(self, event: QMouseEvent):
        if self.__is_recording:
            frame: ndarray = self.client.last_frame
            if frame is None:
                return
            self.__mouse_records.put(MouseRecord(event.pos(), frame))

    def on_process_started(self):
        self.logger.debug(msg="thread started", sender=self.processor)

    def on_processor_saved(self, name: str, x: int, y: int):
        self.logger.success(msg=f"Mouse Click Event Recorded: {name=} ({x=}, {y=})", sender=self.processor)

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
