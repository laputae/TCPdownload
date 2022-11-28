#!/usr/bin/env python
from socket import *
from TCPpack import recvall,get_block,put_block
import re

def main():
    client = socket(AF_INET, SOCK_STREAM)  # 创建socket
    address = ("127.0.0.1", 8889)  # IP&port
    client.connect(address)  # 与服务器建立连接
    while True:  # 一个客户端可以下载多份文件
        name = input("请输入要下载的的文件名（输入quit退出）：")  # 提示用户输入文件名
        # 用户退出
        if name == 'quit':
            client.send(name.encode("utf-8"))
            break
        try:
            fileName = name.split(" ", 1)[0]
            savename = name.split(" ", 1)[1]
        except IndexError:
            print('输入有误')
            continue
        client.send(fileName.encode("utf-8"))  # 发送文件名
        # 接收服务器发送过来的数据
        content=get_block(client)
        if content:
            # 以二进制格式打开一个文件只用于写入
            with open("D:/TCPreceive/" + savename, "wb") as f:
                f.write(content)  # 写入文本
            print("下载完成")
        else:
            print('文件不存在')

    # 关闭套接字
    client.close()


if __name__ == '__main__':
    main()