import ctypes
import socket
import json
from snap7.common import check_error, load_library
from snap7.types import SrvEvent
import snap7.server as server
from typing import Any, Callable, Optional
from dataclasses import dataclass, asdict
import httpx

@dataclass(kw_only=True)
class Message:
    code: int
    message: str
    data: str
    # def __init__(self):
    #     self.code = 200
    #     self.message = ""
    #     self.data = ""


class MySnapServer(server.Server):
    def __init__(self, log: bool = True):
        super().__init__(log)
        self.server_ip = '127.0.0.1'
        self.server_port = 102
        # self.library = load_library()
        # self._read_callback = None
        # self.pointer = None
        # self.library = load_library()
        self.create()
        if log:
            self._set_log_callback()


    def pick_event(self) -> Optional[SrvEvent]:
        event = SrvEvent()
        ready = ctypes.c_int32()
        code = self.library.Srv_PickEvent(self.pointer, ctypes.byref(event),
                                          ctypes.byref(ready))
        check_error(code)
        message = Message(code=2000, message="", data="")
        code_map: dict[int, str] = {
            0x8: "Client added",
            0x80000: "The client requires a PDU",
            0x20000: "Read request",
            0x40000: "Write request",
            0x4000000: "CPU Control request : Warm START/STOP",
            0x400000: "Block upload requested",
            0x80: "Client disconnected", 
            0x10000: "PDU incoming"
        }
        if ready:
            message = Message(code=2000, message="", data=code_map[event.EvtCode])
            self.post_message(message)
            # self.send_tcp_message(json.dumps(message))

            return event

    # def send_udp_message(self, message: str):
    #     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     try:
    #         udp_socket.sendto(message.encode(), (self.server_ip, self.server_port))
    #     except socket.error as e:
    #         print(f"Socket error: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    #     finally:
    #         udp_socket.close()

    # def send_tcp_message(self, message: str, server_address=('localhost', 12345), receive_response=False):
    #     # 参数验证
    #     if not isinstance(message, str):
    #         raise ValueError("Message must be a string")

    #     # 创建socket并确保最终关闭
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #         try:
    #             client_socket.connect(server_address)
    #             client_socket.sendall(message.encode('utf-8'))

    #             if receive_response:
    #                 # 接收响应（如果需要）
    #                 data = client_socket.recv(1024)
    #                 print('Server response:', data.decode('utf-8'))

    #         except Exception as e:
    #             print(f"An error occurred: {e}")

    def post_message(self, message: Message):
        httpx.post(
            url="",
            data=asdict(message)
        )
