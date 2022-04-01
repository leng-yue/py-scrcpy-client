"""
公共方法
"""
import struct
import cv2
import signal
import functools
import numpy as np
from loguru import logger

def unpack_split(bdata):
    if len(bdata) < 30 and b"___" in bdata:
        len_img, serialno = bdata.split(b"___")
        return len_img.decode(), serialno.decode()
    else:
        return 0, ''

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
    return uint8img.tobytes() if sign else b''

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