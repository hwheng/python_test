import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DB_BASE_PATH = os.path.join(BASE_PATH, "db", 'users.xlsx')


USER_FOLDER_PATH = os.path.join(BASE_PATH, 'files')

HOST = "127.0.0.1"
PORT = 8088

