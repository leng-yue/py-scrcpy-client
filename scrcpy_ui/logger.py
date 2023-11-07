import dataclasses
import time
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from .ui import Ui_Logger


@dataclasses.dataclass
class ColorOption:
    info: str
    warn: str
    error: str
    debug: str
    critical: str
    success: str

    def get_color(self, level):
        return getattr(self, level)


class Logger(QWidget):
    instance = None
    onLog = Signal(str)

    def __init__(self, color_option: ColorOption):
        super().__init__()
        self.ui = Ui_Logger()
        self.ui.setupUi(self)
        self.ui.textBrowser.setReadOnly(True)
        self.color_option = color_option or ColorOption(
            info="black",
            warn="orange",
            error="red",
            debug="blue",
            critical="red",
            success="green",
        )
        self.setWindowFlag(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Logger")

        self.setMinimumSize(500, 600)
        self.onLog.connect(self.ui.textBrowser.append)

    @classmethod
    def get_logger(cls, color_option: Optional[ColorOption] = None):
        if not cls.instance:
            cls.instance = Logger(color_option)
        return cls.instance

    @classmethod
    def info(cls, msg, sender=None):
        cls.log(msg, "info", sender)

    @classmethod
    def warn(cls, msg, sender=None):
        cls.log(msg, "warn", sender)

    @classmethod
    def error(cls, msg, sender=None):
        cls.log(msg, "error", sender)

    @classmethod
    def debug(cls, msg, sender=None):
        cls.log(msg, "debug", sender)

    @classmethod
    def critical(cls, msg, sender=None):
        cls.log(msg, "critical", sender)

    @classmethod
    def success(cls, msg, sender=None):
        cls.log(msg, "success", sender)

    @classmethod
    def log(cls, msg, level, sender):
        instance = cls.instance
        instance.__log(msg, level, sender)

    def __log(self, msg, level, sender):
        instance = self
        sender = (sender or instance).__class__.__name__
        if not instance:
            raise RuntimeError(
                "Logger instance is not initialized. use Logger.get_instance() instead."
            )
        # time + Level + msg
        log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        color = instance.color_option.get_color(level)
        if level != "critical":
            msg = f'<font color="{color}">{log_time} [{level.upper()}] {sender}::{msg}</font>'
        else:
            # bold
            msg = f'<font color="{color}"><b>{log_time} [{level.upper()}] {sender}::{msg}</b></font>'
        self.onLog.emit(msg)