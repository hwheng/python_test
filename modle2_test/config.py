import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.get_download_csv import download_video

#获取跟目录路径
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

#csv文件路径
CSV_FILE_PATH = os.path.join(BASE_PATH, 'db')

#下载文件路径            
DOWNLOAD_FILE_PATH = os.path.join(BASE_PATH, 'files')

#检查db目录是否有文件，如果没有执行下载文件
path =  os.path.exists(f'{CSV_FILE_PATH}\Video.csv')
if path == False:
    print('正在配置视频资讯平台....')
    download_video()
    
with open(f'{CSV_FILE_PATH}\Video.csv','r',encoding='utf-8') as file_object:
    LINE_IN_CSV = []
    for line in file_object:
        LINE_IN_CSV.append(line)
    LEN_LINE_IN_CSV = len(LINE_IN_CSV)
