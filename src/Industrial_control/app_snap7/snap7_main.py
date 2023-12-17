import snap7
from snap7.types import (
    wordlen_to_ctypes, 
    WordLen, 
    srvAreaCT,
    srvAreaDB,
    srvAreaMK,
    srvAreaPA,
    srvAreaPE,
    srvAreaTM
)
# from snap7.util import *
import time
import logging

from MySnapServer import MySnapServer



def snap_main(tcpport: int = 102, init_standard_values: bool = False):
    server = MySnapServer()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    size = 150
    DBdata = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    PAdata = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    TMdata = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    CTdata = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    MKdata = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    PEdata = (wordlen_to_ctypes[WordLen.Byte.value] * size)()
    server.register_area(srvAreaDB, 1, DBdata)
    server.register_area(srvAreaPA, 1, PAdata)
    server.register_area(srvAreaTM, 1, TMdata)
    server.register_area(srvAreaCT, 1, CTdata)
    server.register_area(srvAreaMK, 1, MKdata)
    server.register_area(srvAreaPE, 1, PEdata)

    if init_standard_values:
        ba = snap7.server._init_standard_values()
        DBdata = wordlen_to_ctypes[WordLen.Byte.value] * len(ba)
        DBdata = DBdata.from_buffer(ba)
        server.register_area(srvAreaDB, 0, DBdata)
    server.start_to("0.0.0.0",tcpport)
    while True:
        while True:
            event = server.pick_event()
            if event:
                pass
            else:
                break
        time.sleep(1)

if __name__ == '__main__':
    snap_main()


