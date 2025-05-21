import socket as s
from threading import Thread

HOST = ''
PORT = 6754

class PrintReceiveData(Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        print("[+] Receiver thread started.")
        try:
            while True:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode().strip()
                if message.lower() in ['quit', 'exit']:
                    print('{}:{} requested to close the connection.'.format(addr[0], addr[1]))
                    continue  # still listen to others
                print("{} => {}".format(addr[0], message))
        except Exception as e:
            print('Error in receiving thread: {}'.format(e))

sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))

print("[+] UDP Server started on port {}".format(PORT))

try:
    thread = PrintReceiveData(sock)
    thread.start()

    while thread.is_alive():
        thread.join(1)

except KeyboardInterrupt:
    print("\n[!] Server shutting down...")

finally:
    sock.close()
    print("[-] Server socket closed")
