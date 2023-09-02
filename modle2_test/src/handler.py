'''接口程序
调用utils.download（下载模块）、utils.search（搜索模块）和utils.page（分页看新闻模块）
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
import config
from utils.download import download_ready
from utils.search import search_ready
from utils.page import news_ready
from utils.get_download_csv import download_video


def yes():
    download_video()
    while True:
        print('本平台包含三个模块：\n1.分页看新闻模块\n2.搜索模块\n3.视频下载模块')
        user_info_y = input('请选择需要使用的功能：（退出请输入Q/q）')
        if user_info_y.upper() == 'Q':
            print('bye~~')
            bye = 1
            return bye
        user_info_y_group = re.match('(1|2|3)',user_info_y.strip())
        if not  user_info_y_group:
            print('无法识别该模块，请重新输入...')
        num_y = int(user_info_y)
        if num_y == 1:
            back = news_ready()
            if back == 1:
                continue
        if num_y == 2:
            back = search_ready()
            if back == 1:
                continue
        if num_y == 3:
            download_ready()
            if back == 1:
                continue
def no():  
    while True:
        print('本平台包含三个模块：\n1.分页看新闻模块\n2.搜索模块\n3.视频下载模块')
        user_info_n = input('请选择需要使用的功能：（退出请输入Q/q）')
        if user_info_n.upper() == 'Q':
            print('bye~~')
            bye = 1
            return bye
        user_info_n_group = re.match('(1|2|3)',user_info_n.strip())
        if not user_info_n_group:
            print('无法识别该模块，请重新输入...')
        num_n = int(user_info_n)
        if num_n == 1:
            back = news_ready()
            if back == 1:
                continue
        if num_n == 2:
            back = search_ready()
            if back == 1:
                continue
        if num_n == 3:
            download_ready()
            if back == 1:
                continue


def start():
    print('欢迎来到短视频资讯平台，请问是否要更新最新的视频咨询？')
    while True:
        info = input('请进行更新：（输入Y/N确定是否进行更新，退出请输入Q/q）')
        if info.upper() == 'Q':
            print('bye~~')
            return
        info_group = re.match('(Y|N)',info.strip().upper())
        if not info_group:
            print('格式错误，请重新输入')
            continue
        if info.upper() == 'Y':
            bye = yes()
        if info.upper() == 'N':
            bye = no()
        if bye:
            return





