#!/usr/bin/env python
# 单线程，迭代服务器
#(依次服务每一个客户端)
from TCPpack import recvall,get_block,put_block
from socket import *


def get_filecontent(fileName):
    '''读取文件内容'''
    try:
        # open()以二进制格式打开一个文件用于只读
        with open('D:/TCPfiletransport/' + fileName, "rb") as f:
            # read() 每次读取整个文件，将文件内容放到一个字符串变量中
            content = f.read()
            return content  # 文本
    except (FileNotFoundError,PermissionError):
        print("没有找到文件")
        return


def handle(client_socket):
    '''负责和客户端之间的通信'''
    print("有新的客户端建立连接")
    print("服务器信息：", client_socket.getpeername())
    print("客户端信息：", client_socket.getsockname())
    while True:  # 不断接收用户的下载请求
        # 接收客户端发送的文件名
        recv_data = client_socket.recv(1024).decode('utf-8')
        # 客户端请求退出
        if recv_data == 'quit':
            client_socket.close()  # 关闭套接字
            print("客户端已退出")
            break

        print("客户端请求下载的文件名为:" + recv_data)
        # 获取并发送文件长度+内容
        if get_filecontent(recv_data):
            myfile = get_filecontent(recv_data)
            put_block(client_socket,myfile)
            print("已发送"+recv_data+"给客户端")
        else:  # 发送0代表没有找到文件
            client_socket.send('0'.encode("utf-8"))


def main():
    server = socket(AF_INET, SOCK_STREAM)  # 创建socket
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)  # 设置端口复用
    address = ('', 8889)  # 本地信息
    server.bind(address)  # 绑定
    # 使用socket创建的套接字默认是主动模式，将其变为被动模式，接收客户端连接请求
    server.listen(128)  # 128可以监听的最大数量，最大链接数

    while True:
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字
        # client_socket用来为这个客户端服务
        # server等待其他客户端的链接
        client_socket, client_addr = server.accept()
        handle(client_socket)


if __name__ == '__main__':
    main()