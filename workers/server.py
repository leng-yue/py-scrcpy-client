import socket
import time

from loguru import logger

from .schemas import RspInfo
from .utils import StructPack, imdecode


class UDPServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def do_some_things(self, addr, seriano, bimg):
        img = imdecode(buint8img=bimg)
        if img is None:
            return
        # region fork work
        logger.info(f"接收到来自{addr}({seriano})的画面{img.shape}，正在处理...")
        # import cv2

        # cv2.imshow(f"test__{seriano}_{int(time.time())}.png", img)
        # cv2.waitKey(1)
        # time.sleep(0.01)
        # endregion
        resp = RspInfo(
            utime=int(time.time()),
            rst={"msg": "ok", "action": None, "seriano": seriano},
        )
        self.server.sendto(resp.encode(), addr)

    def run(self, host: str, port: int):
        while 1:
            try:
                self.server.bind((host, port))
            except:
                print("ohhhhhhhhhhhhhhhhhhhhhh!")
                time.sleep(10)
            dict_imgs = {}
            while 1:
                recvinfo = self.server.recvfrom(1024)
                bdata, addr = recvinfo
                unpack_data = StructPack.struct_unpack(bdata)
                data_size = unpack_data[0]
                seriano = unpack_data[1]

                if len(bdata) == StructPack.HeadLenth:
                    logger.debug(f"get new img, size: {data_size}")
                    dict_imgs[seriano] = {"len": data_size, "bimg": b""}
                elif seriano in [i for i in dict_imgs.keys()]:
                    dict_imgs[seriano]["bimg"] += bdata[StructPack.HeadLenth :]
                    if len(dict_imgs[seriano]["bimg"]) == dict_imgs[seriano]["len"]:
                        self.do_some_things(addr, seriano, dict_imgs[seriano]["bimg"])
                        del dict_imgs[seriano]
