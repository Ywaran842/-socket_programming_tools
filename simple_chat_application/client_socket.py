from threading import Thread
from socket import socket as SockType, AF_INET, SOCK_STREAM
from pathlib import Path
import sys
import select

class ClientSock(Thread):
    def __init__(self, username: str, sock_module: type, host: str, port: int):
        super().__init__()
        self.username = username
        self.sock_module = sock_module
        self.host = host
        self.port = port

    def print_receive_data(self, sock: SockType):
        try:
            while True:
                data = sock.recv(1024).decode().strip()
                if not data:
                    break
                if data:
                    try:
                        user, message = data.split(',', 1)
                        user = user.strip().lower()
                        print('{} => {}'.format(user, message))
                    except ValueError:
                        print(data)
                
        except Exception as e:
            print("[!] Error receiving data: {}".format(e))
        finally:
            sock.close()

    def client(self):
        try:
            sock = self.sock_module.socket(AF_INET, SOCK_STREAM)
            sock.connect((self.host, self.port))
            print('Connected to server {}:{}'.format(self.host, self.port))
            sock.sendall(self.username.encode())

            # Start thread to receive messages
            thread = Thread(target=self.print_receive_data, args=(sock,), daemon=True)
            thread.start()

            while thread.is_alive():
                # Wait for input or thread exit
                ready, _, _ = select.select([sys.stdin], [], [], 1)
                if ready:
                    data = sys.stdin.readline().strip()
                    if data.lower() in ['exit', 'quit']:
                        sock.sendall(data.encode())
                        print("[!] Exiting...")
                        break
                    sock.sendall(data.encode())
                # If thread is not alive, break
                if not thread.is_alive():
                    print("[!] Server disconnected exiting...")
                    break

        except ConnectionRefusedError:
            print("[!] Server is not running or refused the connection.")
        except KeyboardInterrupt:
            print("\n[!] Interrupted by user.")
        finally:
            if not sock._closed():
                sock.close()

    def run(self):
        try:
            self.client()
        except:
            pass
