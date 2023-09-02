'''
搜索专区
- 用户输入关键字，根据关键词筛选出所有匹配成功的短视频资讯。
- 支持的搜索两种搜索格式：
  - `id=1715025`，筛选出id等于1715025的视频（video.csv的第一列）。
  - `key=文本`，模糊搜索，筛选包含关键字的所有新闻（video.csv的第二列）。
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
import config



def id_serch():
    '''ID精准搜索'''
    while True:
        id_search_info = input('请输入目标视频ID:(输入Q/q返回上一级)')
        if id_search_info.upper() == 'Q':
            return
        # 获取输入的数字，如果输入的数字为7位存储进num_group中
        id_group = re.match('\d{7}',id_search_info.strip())
        if not id_group:
            print('格式错误，请重新输入')
            continue
        with open(f'{config.CSV_FILE_PATH}\Video.csv','r',encoding='utf-8') as file_object:
            for line in file_object:
                line = line.strip().split(',')
                id = line[0]
                if id_search_info == id:
                    title = line[1]
                    print(title)
                    continue

def mumble_search():
    '''模糊搜索'''
    while True:
        mumble_info = input('请输入搜索关键词:(输入Q/q返回上一级)')
        if mumble_info.upper() == 'Q':
            return
        # 获取输入的内容，如果输入的内容不包含特殊字符就存储进mumble_group中
        mumble_group = re.match('\w+',mumble_info.strip())
        if not mumble_group:
            print('格式错误，请重新输入')
            continue
        title_list = []
        with open(f'{config.CSV_FILE_PATH}\Video.csv','r',encoding='utf-8') as file_object:
            for line in file_object:
                title = line.strip().split(',')[1]
                if mumble_info in title:
                    title_list.append(title)
        # title_list存储了包含关键字的索引，如果title_list为空，那么需要重新搜索
        if not title_list:
                print('查询该关键字暂时没有结果，请重新输入...')
                continue
        for data in title_list:
            print(data)
            continue
            

def search_ready():
    print('欢迎来到搜索专区^w^\n目前搜索专区支持的搜索两种搜索格式：\n1.通过ID搜索\n2.模糊搜索')
    while True:
        info = input('请选择搜索格式：1.通过ID搜索 2.模糊搜索(输入Q/q返回上一级)')
        if info.upper() == 'Q':
            back = 1
            return back
        if not info.isdecimal():
            print('格式错误，请重新输入...')
            continue
        num = int(info)
        if num == 1:
            id_serch()
        if num == 2:
            mumble_search()

        
