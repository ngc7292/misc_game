#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/10/31'
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

import socket
import numpy as np
import json
from multiprocessing import Process
import hashlib
import requests
import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }

    def __init__(self,filename,level='info',when='D',backCount=30,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
        
access_log = Logger(filename="access.log")
error_log = Logger(filename="error.log",level='error')
success_log = Logger(filename="success.log")

START_TXT = """



 _______ _________ _______  _______    _______  _______  _______  _______
(       )\__   __/(  ____ \(  ____ \  (  ____ \(  ___  )(       )(  ____ \\
| () () |   ) (   | (    \/| (    \/  | (    \/| (   ) || () () || (    \/
| || || |   | |   | (_____ | |        | |      | (___) || || || || (__
| |(_)| |   | |   (_____  )| |        | | ____ |  ___  || |(_)| ||  __)
| |   | |   | |         ) || |        | | \_  )| (   ) || |   | || (
| )   ( |___) (___/\____) || (____/\  | (___) || )   ( || )   ( || (____/\\
|/     \|\_______/\_______)(_______/  (_______)|/     \||/     \|(_______/



this is a sample eazy game and i will give you a lot of numbers and you can
check them and get the flag, every level means some info of flag.

hint is here!!!!

input y to start this game, and input hint to get hint:
"""

HINT_TXT = """


the flag hidden in these data,
the data come form:

#!/usr/bin/env python

def divide_flag(token):
    flag_list = []
    flag = "********************************"
    for i in range(0,32,2):
        flag_list.append(int(flag[i]+flag[i+1],16))
    return flag_list
    
def game(level,flag_list):
    
    level = level*4
    freq_list = flag_list[level:level+4]
    
    x = np.linspace(0,1,1500)
    y = []
    for freq in freq_list:
        if y == []:
            y = get_number(x,freq,7)
        else:
            y += get_number(x,freq,7)
    return y,freq_list

"""

CONGRATULATION_TXT = """

congratulations ,you solve the whole game and flag is :

hctf{ ''.join([hex(freq) for freq in every freq you get]) }

totle length of whole flag whithout hctf{} is 32

"""

flag_list = []

def server():
    host = "127.0.0.1"
    port = 6775
    BUFFSIZE = 1024
    
    ADDR = (host,port)
    
    server_conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_conn.bind(ADDR)
    server_conn.listen(4096)
    access_log.logger.info("server bind in"+str(ADDR))
    
    
    while True:
        tcpClisock , cli_addr = server_conn.accept()
        access_log.logger.info("accept client "+ str(cli_addr))
        
        p = Process(target=problem,args=(tcpClisock,cli_addr))
        p.start()
        
def problem(tcpClisock,cli_addr):
    tcpClisock.sendall(START_TXT.encode("utf-8"))
    data = tcpClisock.recv(1024)
    data = data.decode("utf-8").replace("\n","")
    if data == "hint":
        tcpClisock.sendall(HINT_TXT.encode("utf-8"))
        tcpClisock.close()
    elif data == "y":
        tcpClisock.sendall("input your token:".encode("utf-8"))
        token = tcpClisock.recv(1024).decode("utf-8").replace("\n","")
        if check_token(token) == True:
            access_log.logger.info("token "+str(token)+" access in")
            start_game(tcpClisock,token)
        else:
            tcpClisock.sendall("your token is error".encode("utf-8"))
            tcpClisock.close()
    else:
        tcpClisock.close()
        
def divide_flag(token):
    flag_list = []
    flag_salt = "fFt_Is_5o_Ea2y"
    flag = hashlib.md5(str(token+flag_salt).encode("utf-8")).hexdigest()
    for i in range(0,32,2):
        flag_list.append(int(flag[i]+flag[i+1],16))
    return flag_list

def check_token(token):
    try:
        url = "https://hctf.io/API/token/"+token
        data = requests.get(url).text
        data = json.loads(data)
        return True if data["status"] == "success" else False
    except BaseException as e:
        error_log.logger.error(e)
        error_log.logger.error(token)
        

def get_verify():
    pass

def start_game(tcpClisock,token):
    
    flag_list = divide_flag(token)
    
    level = 0
    while True:
        if level == 4:
            tcpClisock.sendall(CONGRATULATION_TXT.encode("utf-8"))
            success_log.logger.info(str(token)+" get the flag")
            break
        y,freq_list = game(level,flag_list)
        send_data = json.dumps(list(y)).encode("utf-8")
        tcpClisock.sendall(send_data)
        req_data = tcpClisock.recv(1024).decode("utf-8").replace("\n","")
        req = req_data.split(" ")
        req.sort()
        freq_list.sort()
        if req == freq_list:
            level += 1
            continue
        else:
            break
    tcpClisock.close()
        

def game(level,flag_list):
    
    level = level*4
    freq_list = flag_list[level:level+4]
    
    x = np.linspace(0,1,1500)
    y = []
    res = []
    for freq in freq_list:
        if y == []:
            y = get_number(x,freq,7)
        else:
            y += get_number(x,freq,7)
        res.append(str(freq))
    return y,res


def get_number(x, freq,rge):
    y = np.sin(2*np.pi*x*freq)*rge
    return y
    
if __name__ == '__main__':
    server()