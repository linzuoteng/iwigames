import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages')
import socket
import threading

class Server():#サーバー側(受信側の処理)
    def __init__(self,q, host, port):
        self.q = q
        self.host = host
        self.port = port
        
        self.bufsize = 1024

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.thread = threading.Thread(target = self.c2s, daemon=True)
        self.thread.start()

    def c2s(self):#サーバー側へ受信
        try:
            while True:
                msg, cli_addr = self.sock.recvfrom(self.bufsize)
                msg.decode('utf-8')
                self.q.put(msg)

        except Exception as e:
            print(e)
    