import json
import os
import re
import socket
from modle3_text.client.config import seting
from modle3_text.client.utils import req

class Client:

    def __init__(self):
        self.host = seting.HOST
        self.port = seting.PORT
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def start(self):
        self.conn.connect((self.host, self.port))
        welcome = """
        欢迎使用网盘系统，相关指令如下：
        登录：login 用户名 密码
        注册：register 用户名 密码
        查看：ls 目录
        上传：upload 本地路径 远程路径
        下载：download 本地路径 远程路径
        删除：delete 远程目录
        创建：mkdir 远程目录    
        """
        print(welcome)

        function_map = {
            'login': self.login,
            'register': self.register,
            'ls': self.show,
            'upload': self.upload,
            'download': self.download,
            'delete': self.delete,
            'mkdir': self.mkdir,
        }
        while True:
            hint = f"{self.username or '未登录'}>>>"
            info = input(hint).strip()
            if not info:
                print('输入不能为空，请重新输入')
                continue

            if info.upper() == 'Q':
                print('账号退出登录')
                req.send_data(self.conn, 'q')
                break

            cmd,*args = re.split(r'\s+',info)
            function = function_map.get(cmd)
            if not function:
                print('命令不存在，请重新输入')
                continue
            function(*args)
        self.conn.close()

    def login(self, *args):
        if len(args) != 2:
            print('格式错误，请重新输入')
            return

        username, password = args
        req.send_data(self.conn, f'login {username} {password}')
        repaly = req.recv_data(self.conn).decode('utf-8')
        replay_dict = json.loads(repaly)
        if replay_dict['status']:
            self.username = username
            print(replay_dict['data'])
            return
        print(replay_dict['error'])

    def register(self, *args):
        if len(args) != 2:
            print('格式错误，请重新输入')
            return
        username, password = args
        req.send_data(self.conn,f'register {username} {password}')
        repaly = req.recv_data(self.conn).decode('utf-8')
        replay_dict = json.loads(repaly)
        if replay_dict['status']:
            print(replay_dict['data'])
            self.username = username
            return
        print(replay_dict['error'])

    def show(self, *args):
        if not self.username:
            print('未登录系统，请登录后查看')
            return
        if not args:
            # print(args)
            cmd = 'ls'
            # print(cmd)
        elif len(args) == 1:
            cmd = 'ls {}'.format(*args)
        else:
            print("格式错误，请重新输入。提示：ls 或 ls 目录 ")
            return
        # print(cmd, self.conn)
        req.send_data(self.conn, cmd)
        replay = req.recv_data(self.conn).decode('utf-8')
        repaly_dict = json.loads(replay)
        if repaly_dict['status']:
            print(repaly_dict['data'])
            return
        print(repaly_dict['error'])

    def upload(self, *args):
        if not self.username:
            print('未登录系统，请登录后查看')
        if len(args) != 2:
            print("格式错误，请重新输入。提示：upload 本地路径 远程路径")
            return
        locale_file_path, targe_file_path = args
        if not os.path.exists(locale_file_path):
            print(f'文件路径{locale_file_path}不存在，请重新输入')
            return
        if os.path.isdir(targe_file_path):
            print(f'{targe_file_path}是一个文件夹，上传文件需要写入文件路径，请重新输入')
            return

        req.send_data(self.conn, f'upload {targe_file_path}')
        repaly = req.recv_data(self.conn).decode('utf-8')
        replay_dict = json.loads(repaly)
        if not replay_dict['status']:
            print(replay_dict['error'])
            return
        else:
            print(replay_dict['data'])
        req.send_file(self.conn, locale_file_path)
        down_repaly = req.recv_data(self.conn).decode('utf-8')
        down_repaly_dict = json.loads(down_repaly)
        print('上传完毕')

    def download(self, *args):
        if not self.username:
            print("登录后才允许下载")
            return
        if len(args) != 2:
            print("格式错误，请重新输入。提示：download 本地目录 远程目录")
            return

        local_file_path, remote_file_path = args
        seek = 0

        if not os.path.exists(local_file_path):
                # download v1.txt
                req.send_data(self.conn, "download {}".format(remote_file_path))
                mode = 'wb'

        else:
                choice = input("是否续传（Y/N) ")
                if choice.upper() == 'Y':
                    # download v1.txt 100
                    seek = os.stat(local_file_path).st_size
                    req.send_data(self.conn, "download {} {}".format(remote_file_path, seek))
                    mode = 'ab'

                else:
                    # download v1.txt
                    req.send_data(self.conn, "download {}".format(remote_file_path))
                    mode = 'wb'


        reply = req.recv_data(self.conn).decode('utf-8')
        reply_dict = json.loads(reply)
        if not reply_dict['status']:
            print(reply_dict['error'])
        else:
            print("开始下载")  # print(reply_dict['data'])
            req.recv_save_file(self.conn, local_file_path, mode, seek=seek)
            print("下载完毕")

    def delete(self, *args):
        if not self.username:
            print('未登录系统，请登录后查看')
        if len(args) == 1:
            cmd = 'delete {}'.format(*args)
        else:
            print("格式错误，请重新输入。提示：delete 目录")

        req.send_data(self.conn, cmd)
        replay = req.recv_data(self.conn).decode('utf-8')
        repaly_dict = json.loads(replay)
        if repaly_dict['status']:
            print(repaly_dict['data'])
            return
        print(repaly_dict['error'])

    def mkdir(self, *args):
        if not self.username:
            print('未登录系统，请登录后查看')
        if len(args) == 1:
            cmd = 'mkdir {}'.format(*args)
        else:
            print("格式错误，请重新输入。提示：delete 目录")

        req.send_data(self.conn, cmd)
        replay = req.recv_data(self.conn).decode('utf-8')
        repaly_dict = json.loads(replay)
        if repaly_dict['status']:
            print(repaly_dict['data'])
            return
        print(repaly_dict['error'])




