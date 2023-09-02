import socket

sock = socket.socket()
sock.bind(("127.0.0.1", 8888))
sock.listen(5)

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024)
    print("has data...")
    with open('index.html', 'r',encoding='utf-8') as f:
        data_html = f.read()
        # 请求头 \r\n 响应头 \r\n\r\n 请求体 data_html = f.read(): 读取文件内容
        conn.send(f'HTTP/1.1 200 ok \r\n Content_Length:11 \r\n\r\n {data_html}'.encode())
    conn.close()
