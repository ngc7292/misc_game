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
from multiprocessing import Process
import math

token = "TN3OWQKHPNmPshbridfU21Sz2LncsJaR"

def solution():
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
        res_y = []
        for i, j in zip(xf2, yf2):
            if int(j) != 0:
                a = math.ceil(yf2[i]*2)
                while a >= 7:
                    res.append(str(i))
                    res_y.append(str(a))
                    a = a//2
                
        return res,res_y
    
    
    tcpCliSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcpCliSock.connect(("127.0.0.1",6775))
    
    
    tcpCliSock.recv(1024)
    tcpCliSock.sendall("y".encode("utf-8"))
    tcpCliSock.recv(1024)
    tcpCliSock.sendall(token.encode("utf-8"))
    
    flag_list = []
    
    
    while True:
        number_data = ""
        while True:
            data = tcpCliSock.recv(65536)
            if data == b'':
                break
            print(data)
            if "con" in data.decode("utf-8"):
                break
            elif "[" in data.decode("utf-8") and "]" in data.decode("utf-8"):
                number_data = data.decode("utf-8")
                break
            elif "[" in data.decode("utf-8"):
                number_data = data.decode(("utf-8"))
            elif "]" in data.decode("utf-8"):
                number_data += data.decode("utf-8")
                break
            else:
                number_data += data.decode("utf-8")
                
        if "con" in data.decode("utf-8"):
            break
        data = number_data
        print(data)
        # print(len(data))
        # print(data)
        data = json.loads(data)
        y = np.array(data)
        res, res_y  = get_freq(x,y)
        while len(res) < 4:
            res = ["0"] + res
        res = " ".join(res)
        print(res, res_y)
        flag_list += res.split(" ")
        tcpCliSock.sendall(res.encode("utf-8"))

if __name__ == '__main__':
    solution()