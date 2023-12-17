import logging
import socket
import os
import time
import threading

from pymodbus.server.async_io import StartTcpServer
from pymodbus.datastore import ModbusServerContext, ModbusSequentialDataBlock, ModbusSlaveContext

file_path = 'modbus.log'


def send_tcp_message(message: str, server_address=('localhost', 12345), receive_response=False):
    # 参数验证
    if not isinstance(message, str):
        raise ValueError("Message must be a string")

    # 创建socket并确保最终关闭
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect(server_address)
            client_socket.sendall(message.encode('utf-8'))

            if receive_response:
                # 接收响应（如果需要）
                data = client_socket.recv(1024)
                print('Server response:', data.decode('utf-8'))

        except Exception as e:
            print(f"An error occurred: {e}")


last_position = 0 # 文件上一次读取的位置


def comm(file_path):
    global last_position
    last_modified_time = os.path.getmtime(file_path)

    while True:
        time.sleep(10)  # 等待10秒
        current_modified_time = os.path.getmtime(file_path)

        if current_modified_time != last_modified_time:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 移动到上次读取的位置
                    file.seek(last_position)

                    # 读取新内容
                    new_content = file.read()
                    if new_content:
                        send_tcp_message(new_content)

                    # 更新读取位置
                    last_position = file.tell()

            except IOError as e:
                print(f"An error occurred while reading the file: {e}")

            # 更新最后修改时间
            last_modified_time = current_modified_time


def modbus_main():
    # crrate Modbus data storage
    datablock = ModbusSequentialDataBlock.create()
    context = ModbusSlaveContext(
        di=datablock,
        co=datablock,
        hr=datablock,
        ir=datablock,
    )
    single = True
    store = ModbusServerContext(slaves=context, single=single)
    address = ("127.0.0.1", 502)

    logging.basicConfig(filename='modbus.log', level=logging.DEBUG)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)
    # 启动TCP通信线程
    thread = threading.Thread(target=comm)
    thread.start()

    StartTcpServer(
        context=store,  # Data storage
        address=address,  # listen address
        identity="ModbusServer"
    )


if __name__ == '__main__':
    modbus_main()
