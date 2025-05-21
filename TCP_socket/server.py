import socket as s
from threading import Thread
import sys

HOST = ''
PORT = 6754

class PrintReceiveData(Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
    
    def run(self):
        try:
            while True:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                if data.strip().lower() in ['quit', 'exit']:
                    print('{}:{} request to close the connection.'.format(addr[0], addr[1]))
                    break
                print("{} => {}".format(self.addr[0], data))
        except Exception as e:
            print('Error with {}: {}'.format(self.addr[0], e))
        finally:
            self.conn.close()
            print("[-] Connection with {} closed".format(self.addr[0]))



sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen()

try:
    while True:
        conn, addr = sock.accept()
        print("{}:{} is connected.".format(addr[0], addr[1]))
        thread = PrintReceiveData(conn, addr)
        thread.start()

except KeyboardInterrupt:
     print("\n[!] Server shutting down.")

finally:
    sock.close()