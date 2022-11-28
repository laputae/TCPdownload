#!/usr/bin/env python
# 异步方式(select模型)
from socket import *
from select import select
from TCPpack import recvall,get_block,put_block

def get_filecontent(fileName):
    '''读取文件内容'''
    try:
        # open()以二进制格式打开一个文件用于只读
        with open('D:/TCPfiletransport/'+fileName, "rb") as f:
            # read() 每次读取整个文件，将文件内容放到一个字符串变量中
            content = f.read()
            return content #文本
    except (FileNotFoundError):
        print("没有找到文件")
        return

def handle(socket,inputs):
    '''负责和客户端之间的通信'''
    # 接收客户端发送的文件名
    recv_data = socket.recv(1024).decode('utf-8')
    # 客户端请求退出
    if recv_data == 'quit':
        inputs.remove(socket) # 从inputs删除套接字
        socket.close() # 关闭套接字
        print("有一个客户端已退出")
        return

    print("客户端请求下载的文件名为:" + recv_data)
    # 获取并发送文件长度+内容
    if get_filecontent(recv_data):
        myfile = get_filecontent(recv_data)
        put_block(socket, myfile)
    else: # 发送''代表没有找到文件
        put_block(socket,''.encode("utf-8"))

def main():
    server = socket(AF_INET, SOCK_STREAM) # 创建socket
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,True) # 设置端口复用
    address = ('', 8889) # 本地信息
    server.bind(address) # 绑定
    # 使用socket创建的套接字默认是主动模式，将其变为被动模式，接收客户端连接请求
    server.listen(128) # 128可以监听的最大数量，最大链接数
    inputs = [server] # 套接字列表，最初只有服务器套接字

    while True:
        # select的原型为(rlist,wlist,xlist,timeout),rlist是等待读取的对象，wlist是等待写入的对象，xlist是等待异常的对象
        read, write, exception = select(inputs, [], [])
        for sock in read:
            if sock == server: # 服务器套接字
                client_socket, client_addr = server.accept() # 有新的客户端连接
                print("有新的客户端建立连接")
                inputs.append(client_socket) # 加入套接字列表
            else: # 连接客户端的套接字
                handle(sock,inputs)

if __name__ == '__main__':
    main()