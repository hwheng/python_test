from modle3_text.server.src import server
from modle3_text.server.src.handels import server_hander


if __name__ == "__main__":
    server_start = server.SelectServer()
    server_start.start(server_hander.Handel)
