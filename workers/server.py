import time
import socket

from loguru import logger

from .utils import imdecode, unpack

from .schemas import RspInfo


class UDPServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def do_some_things(self, addr, bimg):
        img = imdecode(buint8img=bimg)
        if img is None:
            return
        # region fork work
        logger.info(f"接收到来自{addr}的画面{img.shape}，正在处理...")
        import cv2
        cv2.imwrite(f"{addr}_{int(time.time())}.png", img)
        time.sleep(0.01)
        #endregion
        resp = RspInfo(utime=int(time.time()), rst={"msg": "ok", "action": None})
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
                unpack_data = unpack("l", bdata=bdata)

                if unpack_data:
                    data_size = unpack_data[0]
                    logger.debug(f"get new img, size: {data_size}")
                    dict_imgs[addr] = {"len": data_size, "bimg": b''}
                elif addr in [i for i in dict_imgs.keys()]:
                    dict_imgs[addr]["bimg"] += bdata
                    if len(dict_imgs[addr]["bimg"]) == dict_imgs[addr]["len"]:
                        self.do_some_things(addr, dict_imgs[addr]["bimg"])
                        del dict_imgs[addr]