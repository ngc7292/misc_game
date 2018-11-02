#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/30'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃       ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━┓
              ┃神兽保佑┣┓
              ┃永无BUG  ┏┛
              ┗┓┓┏━┳┓┏━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
import requests
import json
import numpy as np
from scipy.fftpack import fft
import socket

token = "rf5LAktSVS0XnOEyC8Z4JoFKQf8X9yln"

x = np.linspace(0,1,1500)

def get_freq(x,y):
    yy = fft(y)
    y_real = yy.real
    y_imag = yy.imag

    yy = abs(fft(y))
    xx = range(len(y))

    yf = abs(fft(y))  # 取绝对值
    yf1 = abs(fft(y)) / len(x)  # 归一化处理
    yf2 = yf1[range(int(len(x) / 2))]  # 由于对称性，只取一半区间

    xf = np.arange(len(y))  # 频率
    xf1 = xf
    xf2 = xf[range(int(len(x) / 2))]  # 取一半区间

    res = []
    for i, j in zip(xf2, yf2):
        if int(j) != 0:
            res.append(str(i))
            
    return " ".join(res)


tcpCliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpCliSock.connect(("127.0.0.1",6775))


tcpCliSock.recv(1024)
tcpCliSock.sendall("y".encode("utf-8"))
tcpCliSock.recv(1024)
tcpCliSock.sendall(token.encode("utf-8"))

flag_list = []
while True:
    data = tcpCliSock.recv(65536)
    if "con" in data.decode("utf-8"):
        break
    print(data)
    data = json.loads(data.decode("utf-8"))
    y = np.array(data)
    res = get_freq(x,y)
    print(res)
    flag_list += res.split(" ")
    tcpCliSock.sendall(res.encode("utf-8"))

flag = ""
for i in flag_list:
    flag += hex(int(i))[2:].zfill(2)

print("hctf{"+flag+"}")
    
