"""
下载梨视频的：视频ID，视频标题，视频URL地址 并写入到本次 video.csv 文件中。

运行此脚本需要预先安装：
    pip install request
    pip install beautifulsoup4

"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from bs4 import BeautifulSoup
import config


def get_mp4_url(video_id):
    data = requests.get(
        url="https://www.pearvideo.com/videoStatus.jsp?contId={}".format(video_id),
        headers={
            "Referer": "https://www.pearvideo.com/video_{}".format(video_id),
        }
    )
    response = data.json()
    image_url = response['videoInfo']['video_image']
    video_url = response['videoInfo']['videos']['srcUrl']
    middle = image_url.rsplit('/', 1)[-1].rsplit('-', 1)[0]
    before, after = video_url.rsplit('/', 1)
    suffix = after.split('-', 1)[-1]
    url = "{}/{}-{}".format(before, middle, suffix)
    return url


def download_video():
    file_object = open(f'{config.CSV_FILE_PATH}\Video.csv', mode='w', encoding='utf-8')
    count = 0
    print('正在更新中....')
    while count <= 999:
        res = requests.get(
            url="https://www.pearvideo.com/category_loading.jsp?reqType=14&categoryId=&start={}".format(count)
        )
        bs = BeautifulSoup(res.text, 'lxml')
        a_list = bs.find_all("a", attrs={'class': "vervideo-lilink"})
        for tag in a_list:
            title = tag.find('div', attrs={'class': "vervideo-title"}).text.strip()
            video_id = tag.get('href').split('_')[-1]
            mp4_url = get_mp4_url(video_id)
            row = "{},{},{}\n".format(video_id, title, mp4_url)
            file_object.write(row)
            file_object.flush()
            count += 1
            i = int(100 * count / 999)
            text = f'\r{i}%'
            print(text,end='')
    print('\n---咨询已更新---')
    file_object.close()


