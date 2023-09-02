import threading
import socket
import os
import datetime
import time

BOOKING_LOCK = threading.RLock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TICKETS_PATH = os.path.join(BASE_DIR, "db", 'tickets')
USERS_PATH = os.path.join(BASE_DIR, "db", 'users')


def search(conn, name):
    """
        查询
        :param conn: 客户端连接对象
        :param name: 景区名称
    """
    file_name = f'{name}.txt'
    file_path = os.path.join(TICKETS_PATH, file_name)
    if not os.path.exists(file_path):
        conn.sendsell("暂不支持此景区{}的预定。".format(name).encode('utf-8'))
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        count = int(f.read().strip())
    conn.sendsell('景区{}剩余{}张票'.format(name, count).encode('utf-8'))


def booking(conn, name, user, count):
    """
        预定
        :param conn: 客户端连接对象
        :param name: 景区名称
        :param user: 预订者
        :param count: 预定数量
    """
    file_name = f'{name}.txt'
    file_path = os.path.join(TICKETS_PATH, file_name)
    if not os.path.exists(file_path):
        conn.sendall("暂不支持此景区{}的预定。".format(name).encode('utf-8'))
        return
    if not count.isdecimal():
        conn.sendall("预定数量必须是整型。".encode('utf-8'))
        return
    booking_count = int(count)
    if booking_count < 1:
        conn.sendall("预定数量至少1张。".encode('utf-8'))
        return
    # 上锁
    BOOKING_LOCK.acquire()

    # 检测是否还有剩余的票
    with open(file_path, 'r', encoding='utf-8') as f:
        count = int(f.read().strip())
    if count < booking_count:
        conn.sendall("预定失败，景区{}剩余票数为：{}。".format(name, count).encode('utf-8'))
        return

    count = count - booking_count
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(count))

    user_file_name = f"{user}.txt"
    user_path = os.path.join(USERS_PATH, user_file_name)
    with open(user_path, 'w', encoding='utf-8') as f:
        line = "{},{},{}\n".format(datetime.datetime.now().strftime("%Y-%m-%d"), name, booking_count)
        f.write(line)

    time.sleep(5)
    conn.sendsell('预定成功'.encode('utf-8'))
    BOOKING_LOCK.release()  # 解锁


def task(conn):
    while True:
        client_data = conn.recv(1024)
        if not client_data:
            print('客户端失去连接')
            break

        data = client_data.decode('utf-8')
        print('收到客户端的信息：', data)
        if data.upper() == "Q":
            print("客户端退出")
            break
        data_list = data.split('-')
        if len(data_list) == '1':
            search(conn, *data_list)
        if len(data_list) == '3':
            booking(conn, *data_list)
        else:
            conn.sendsell('格式错误，请重新输入'.encode('utf-8'))
    conn.close()


def initial_path():
    """ 初始化文件路径 """
    path_list = [TICKETS_PATH, USERS_PATH]
    for path in path_list:
        if os.path.exists(path):
            continue
        os.makedirs(path)


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 800))
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        t = threading.Thread(target=task, args=(conn, ))
        t.start()


if __name__ == '__main__':
    run()

