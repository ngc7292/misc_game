#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/11/8'
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
import numpy as np


def get_number(x, freq, rge):
    y = np.sin(2 * np.pi * x * freq) * rge
    return y


def divide_flag():
    flag_list = []
    flag = "****************************************************************"
    for i in range(0, 64, 2):
        flag_list.append(int(flag[i] + flag[i + 1], 16))
    return flag, flag_list


def game(level, flag_list):
    level = level * 4
    freq_list = flag_list[level:level + 4]
    
    x = np.linspace(0, 1, 1500)
    y = []
    for freq in freq_list:
        if y == []:
            y = get_number(x, freq, 7)
        else:
            y += get_number(x, freq, 7)
    return y, freq_list

flag = divide_flag()
print(game(0,flag))
