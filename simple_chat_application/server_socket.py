from threading import Thread
import socket as SockType
import json
from json.decoder import JSONDecodeError
from pathlib import Path

class ServerSock(Thread):
    def __init__(self, host: str, port: int, socket: SockType, name: str, user_file_path: Path):
        super().__init__()
        self.host= host
        self.port = port
        self.s = socket
        self.sock = None
        self.user_name = name
        self.user_file_path = user_file_path
        self.clients = {}

    def server(self):
        self.sock = self.s.socket(self.s.AF_INET, self.s.SOCK_STREAM)
        self.sock.setsockopt(self.s.SOL_SOCKET, self.s.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def print_receive_data(self, conn: SockType, addr: tuple[str, int]):
        try:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                if data in ['quit', 'exit']:
                    print('{} send the exit request.'.format(self.user_name))
                    break
                if '=>' in data:
                    data  = data.split()
                    if len(data) == 2:
                        send_to_name = data[0]
                        message = data[2]
                        sender = self.clients.get(send_to_name.strip().lower())
                        sender['conn'].sendall(message.encode())
                    else:
                        conn.sendall(b'Invalid message format.')
                conn.sendall(data)
        except Exception as e:
            print('Connection closed with {}'.format(self.user_name))
            print(e)
        finally:
            conn.close()
            self.remove_client_file()

    def remove_client_file(self):
        del self.clients[self.name]
        data = self.read_user_file()
        data.remove(self.user_name)
        with open(self.user_file_path, 'w') as file_obj:
            json.dump(data, file_obj)
            

        
    def read_user_file(self) -> tuple[dict]:
        try:
            with open(self.user_file_path) as file_obj:
                data = json.load(file_obj)
                return data
        except JSONDecodeError:
            data = []
            return data

    def add_client_to_file(self, client_data: tuple[dict]):
        data = self.read_user_file()
        data.append(client_data)
        with open(self.user_file_path, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)


    
    def accept_client(self):
        try:
            while True:
                conn, addr = self.sock.accept()
                #store the client data
                client_data = {
                    self.user_name : {
                    'ip_addr' : addr[0],
                    'port' : addr[1],
                }
                }
                self.clients[self.name] = {
                    "conn" : conn
                }
                self.add_client_to_file(client_data)
                print("{} is connected.".format(self.user_name))
                thread = Thread(target=self.print_receive_data, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
        finally:
            self.sock.close()

    def run(self):
        self.server()
        self.accept_client()