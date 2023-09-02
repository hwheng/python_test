'''
下载专区

- 用户输入视频id，根据id找到对应的mp4视频下载地址，然后下载视频到项目的files目录。

- 视频的文件名为：`视频id-年-月-日-时-分-秒.mp4`
'''

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
from datetime import datetime
import requests

import config

def get_download_video(info_video_id):
    '''获取视频url'''
    with open(f'{config.CSV_FILE_PATH}\Video.csv', 'r', encoding='utf-8') as file_object:    
        for line in file_object:
            row_list = line.strip().split(',')
            video_id = row_list[0]
            url = row_list[2]
            if info_video_id == video_id:
                return url

def download(url,id):
    '''视频下载函数'''
    time = datetime.now().strftime("%Y-%m-%d-%H-%M")
    file_path = os.path.join(f'{config.DOWNLOAD_FILE_PATH}',f"{id}-{time}.mp4")
    res = requests.get(
        url=url
    )
    # 视频总大小（字节）
    file_size = int(res.headers['Content-Length'])
    download_size = 0
    with open(f'{file_path}.mp4', mode='wb') as file_object:
        print('正在下载中....')
        # 分块读取下载的视频文件（最多一次读128字节），并逐一写入到文件中。len(chunk)表示实际读取到每块的视频文件大小。
        for chunk in res.iter_content(128):
            download_size += len(chunk)
            file_object.write(chunk)
            file_object.flush()
            '''视频下载百分比'''
            i = int(100 * download_size / file_size)
            text = f'\r{i}%'
            print(text,end='')
        print("\n下载完成")           
        file_object.close()
    res.close()


def download_ready():
    print('下载专区')
    while True:
        info = input('请输入需要下载的视频或标题文本:(输入Q/q返回上一级)')
        if info.upper() == 'Q':
            back = 1
            return back
        # 获取输入的数字，如果输入的数字为7位存储进num_group中
        num_group = re.match('\d{7}',info.strip())
        if not num_group:
            print('视频序号格式错误，请重新输入...')
            continue     
        url = get_download_video(info)
        if not url:
            print('视频不存在，请重新输入') 
        download(url,info)
