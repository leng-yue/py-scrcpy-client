"""
公共方法
"""
import functools
import signal
import struct

import cv2
import numpy as np
from loguru import logger


class StructPack:
    HeadLenth = 28

    @staticmethod
    def struct_pack(len_data, serialno):
        pack = struct.pack("l20s", len_data, serialno.encode())
        len_pack = len(pack)
        if len_pack != StructPack.HeadLenth:
            return 0, b""
        return len_pack, pack

    @staticmethod
    def struct_unpack(bdata) -> tuple([int, str]):
        unpack = struct.unpack("l20s", bdata[: StructPack.HeadLenth])
        len_data = unpack[0]
        serialno = unpack[1].replace(b"\x00", b"").decode()
        serialno = serialno
        return len_data, serialno


def unpack(format, bdata):
    """
    如果可解 返回数据
    不可解 返回None
    """
    if len(bdata) == 8:
        try:
            return struct.unpack(format, bdata)
        except:
            pass


def imencode(img) -> bytes:
    ext = ".png"
    sign, uint8img = cv2.imencode(ext=ext, img=img)
    return uint8img.tobytes() if sign else b""


def imdecode(buint8img) -> np.ndarray:
    img = None
    try:
        uint8img = np.frombuffer(buint8img, np.uint8)
        img = cv2.imdecode(uint8img, cv2.IMREAD_COLOR)
    except Exception as err:
        logger.warning(err)
    return img


def timeout(sec):
    """
    timeout decorator
    Waring: signal only works in main thread of the main interpreter

    :sec int
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            def _handle_timeout(signum, frame):
                err_msg = f"function: {func.__name__} timeout after {sec} seconds."
                logger.error(err_msg)

            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(sec)
            try:
                rst = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return rst

        return wrapped_func

    return decorator
