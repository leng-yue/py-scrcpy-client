import json
from socket import socket

import cv2
import numpy as np
from loguru import logger
from pydantic import BaseModel

try:
    from .utils import imdecode, imencode
except:

    def imencode(img) -> bytes:
        ext = ".png"
        sign, uint8img = cv2.imencode(ext=ext, img=img)
        return uint8img.tobytes() if sign else b""

    def imdecode(buint8img) -> np.ndarray:
        uint8img = np.frombuffer(buint8img, np.uint8)
        return cv2.imdecode(uint8img, cv2.IMREAD_COLOR)


# from typing import Dict, List, Optional


class ServerInfo(BaseModel):
    host: str
    port: int
    server: socket = None

    class Config:
        arbitrary_types_allowed = True


class ReqInfoSmallImg(BaseModel):
    """
    tips: 小于1024的可以直接发送,一般需要分包发送
    """

    utime: int
    img: np.ndarray
    split_by: bytes = b"utime_img"

    class Config:
        arbitrary_types_allowed = True

    def encode(self):
        endata = b""
        butime = str(self.utime).encode()
        bimg = imencode(self.img)
        if bimg:
            endata = self.split_by.join([butime, bimg])
        else:
            logger.warning(f"ReqInfoSmallImg img can't encode: {self.img.shape})")
        return endata

    @staticmethod
    def decode(bdata):
        data = None
        blist = bdata.split(ReqInfoSmallImg(utime=0, img=np.ndarray(0)).split_by)
        if len(blist) == 2:
            btime, buint8img = blist
            utime = int(btime.decode())
            img = imdecode(buint8img)
            data = ReqInfoSmallImg(utime=utime, img=img)
        return data


class RspInfo(BaseModel):
    utime: int
    rst: dict
    split_by: bytes = b"utime_rst"

    class Config:
        arbitrary_types_allowed = True

    def encode(self) -> bytes:
        endata = b""
        butime = str(self.utime).encode()
        brst = json.dumps(self.rst).encode()

        endata = self.split_by.join([butime, brst])
        return endata

    @staticmethod
    def decode(bdata):
        data = None
        blist = bdata.split(RspInfo(utime=0, rst={}).split_by)
        if len(blist) == 2:
            btime, brst = blist
            utime = int(btime.decode())
            rst = json.loads(brst.decode())
            data = RspInfo(utime=utime, rst=rst)
        return data


if __name__ == "__main__":
    import os
    import time

    def test_reqinfo():
        img_path = os.path.join(os.environ.get("HOME"), "Desktop", "nani.jpeg")
        img = cv2.imread(img_path)
        utime = int(time.time())
        req = ReqInfoSmallImg(utime=utime, img=img)
        endata = req.encode()
        decode = ReqInfoSmallImg.decode(endata)
        assert decode.utime == req.utime and decode.img.all() == req.img.all()

    def test_rspinfo():
        utime = int(time.time())
        req = RspInfo(utime=utime, rst={"test": {"result": [0, 0], "confidence": 1.0}})
        endata = req.encode()
        decode = RspInfo.decode(endata)
        assert req == decode

    test_reqinfo()
    test_rspinfo()
