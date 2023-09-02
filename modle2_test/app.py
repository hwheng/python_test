# import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.handler import start
from utils.get_download_csv import download_video

if __name__ == '__main__':
    start()
