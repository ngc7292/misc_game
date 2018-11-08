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
import os

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
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        
access_log = Logger(filename="access.log")
error_log = Logger(filename="error.log",level='error')
success_log = Logger(filename="success.log")

START_TXT = """
 _______  _______  _______  _______    _______  _______  _______  _______
(  ____ \(  ____ )(  ____ \(  ___  )  (  ____ \(  ___  )(       )(  ____ \\
| (    \/| (    )|| (    \/| (   ) |  | (    \/| (   ) || () () || (    \/
| (__    | (____)|| (__    | |   | |  | |      | (___) || || || || (__
|  __)   |     __)|  __)   | |   | |  | | ____ |  ___  || |(_)| ||  __)
| (      | (\ (   | (      | | /\| |  | | \_  )| (   ) || |   | || (
| )      | ) \ \__| (____/\| (_\ \ |  | (___) || )   ( || )   ( || (____/\\
|/       |/   \__/(_______/(____\/_)  (_______)|/     \||/     \|(_______/


this is a sample game ...

"""

HINT_TXT = """


the flag hidden in these data,
the data come form:

#!/usr/bin/env python

def get_number(x, freq,rge):
    y = np.sin(2*np.pi*x*freq)*rge
    return y
    
def divide_flag(token):
    flag_list = []
    flag = "****************************************************************"
    for i in range(0,64,2):
        flag_list.append(int(flag[i]+flag[i+1],16))
    return flag,flag_list
    
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
    
def start_game(tcpClisock,token,userlogger):
    
    flag,flag_list = divide_flag(token)
    level = 0
    while True:
        if level == 8:
            tcpClisock.sendall((CONGRATULATION_TXT.format("hctf{"+flag+"}")).encode("utf-8"))
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

"""

CONGRATULATION_TXT = """

congratulations ,you solve the whole game and flag is :{0}

"""

flag_list = []

def server():
    host = "0.0.0.0"
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
    file_name = str(cli_addr[0])+".log"
    userlogger = Logger(filename=file_name)
    
    tcpClisock.sendall(START_TXT.encode("utf-8"))
    while True:
        tcpClisock.sendall("\ninput y to start this game, and input hint to get hint:".encode("utf-8"))
        data = tcpClisock.recv(1024)
        data = data.decode("utf-8").replace("\n","")
        userlogger.logger.info("user input: "+str(data))
        if data == "hint":
            tcpClisock.sendall(HINT_TXT.encode("utf-8"))
        elif data == "y":
            tcpClisock.sendall("input your token:".encode("utf-8"))
            token = tcpClisock.recv(1024).decode("utf-8").replace("\n","")
            if check_token(token) == True:
                userlogger.logger.info("token "+str(token)+" access in")
                start_game(tcpClisock,token,userlogger)
                break
            else:
                tcpClisock.sendall("your token is error".encode("utf-8"))
                tcpClisock.shutdown(2)
                break
        else:
            tcpClisock.sendall("your input is error".encode("utf-8"))
            tcpClisock.shutdown(2)
            break
        
def divide_flag(token):
    flag_list = []
    flag_salt = "fFt_Is_5o_Ea2y"
    flag = hashlib.sha256(str(token+flag_salt).encode("utf-8")).hexdigest()
    for i in range(0,64,2):
        flag_list.append(int(flag[i]+flag[i+1],16))
    return flag,flag_list

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

def start_game(tcpClisock,token,userlogger):
    
    flag,flag_list = divide_flag(token)
    level = 0
    while True:
        if level == 8:
            tcpClisock.sendall((CONGRATULATION_TXT.format("hctf{"+flag+"}")).encode("utf-8"))
            
            userlogger.logger.info(str(token)+" get the flag")
            
            break
        y,freq_list = game(level,flag_list)
        send_data = json.dumps(list(y)).encode("utf-8")
        tcpClisock.sendall(send_data)
        req_data = tcpClisock.recv(1024).decode("utf-8").replace("\n","")
        userlogger.logger.info("user recv: "+str(req_data))
        userlogger.logger.info("success freq: "+str(freq_list))
        req = req_data.split(" ")
        req.sort()
        freq_list.sort()
        if req == freq_list:
            level += 1
            continue
        else:
            break
    tcpClisock.shutdown(2)
        

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