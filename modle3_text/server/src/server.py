import socket
import select
import threading
from modle3_text.server.config import seting


class Server:
    """普通服务端"""

    def __init__(self):
        self.host = seting.HOST
        self.port = seting.PORT
        self.lock = threading.RLock()

    def thread_task(self, conn, addr, handel):
        while True:
            # conn, addr, handels = args
            print("[*] 客户端连接地址：", addr)
            instance = handel(conn)
            while True:
                self.lock.acquire()
                result = instance.execute()
                self.lock.release()
                if not result:
                    break
            conn.close()

    def start(self, handel):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.thread_task, args=(conn, addr, handel,), daemon=False)
            t.start()


class SelectServer:
    """基于IO多路复用的服务端"""

    def __init__(self):
        self.host = seting.HOST
        self.port = seting.PORT
        self.server_object_list = []
        self.conn_handler_map = {}

    def start(self, handel):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.setblocking(True)
        server.bind((self.host, self.port))
        server.listen(5)
        self.server_object_list.append(server)
        while True:
            r, w, e = select.select(self.server_object_list, [], [], 0.02)
            for sock in r:
                if sock == server:
                    conn, addr = sock.accept()
                    print("[*] 客户端连接地址：", addr)
                    self.server_object_list.append(conn)
                    self.conn_handler_map[conn] = handel(conn)
                    continue


                handler_object = self.conn_handler_map.get(sock)
                if handler_object:
                    result = handler_object.execute()
                    if not result:
                        self.server_object_list.remove(sock)
                        del self.conn_handler_map[sock]
                else:
                    self.server_object_list.remove(sock)
