### 网盘系统（屎山代码）
- main.py为启动程序
- 配置端口在/config/seting中
```python
# server:
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_BASE_PATH = os.path.join(BASE_PATH, "db", 'users.xlsx')
USER_FOLDER_PATH = os.path.join(BASE_PATH, 'files')
HOST = "127.0.0.1"
PORT = 8088

# client:
HOST = "127.0.0.1"
PORT = 8088
```
- 使用方法：
```
        登录：login 用户名 密码
        注册：register 用户名 密码
        查看：ls 目录
        上传：upload 本地路径 远程路径
        下载：download 本地路径 远程路径
        删除：delete 远程目录
        创建：mkdir 远程目录   
        eg: 上传和下载一定要指向文件路径而不是文件所在目录，例如我要上传一个1.txt文件，
            那么上传指令为： upload 1.txt 1.txt
```