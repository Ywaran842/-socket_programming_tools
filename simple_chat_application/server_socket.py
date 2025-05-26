from threading import Thread
from socket import socket as SockType
import json
from json.decoder import JSONDecodeError
from pathlib import Path

class ServerSock(Thread):
    def __init__(self, host: str, port: int, socket: SockType, user_file_path: Path):
        super().__init__()
        self.host = host
        self.port = port
        self.s = socket
        self.sock = None
        self.user_file_path = user_file_path
        self.clients = {}

    def server(self):
        self.sock = self.s.socket(self.s.AF_INET, self.s.SOCK_STREAM)
        self.sock.setsockopt(self.s.SOL_SOCKET, self.s.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def print_receive_data(self, conn: SockType, addr: tuple[str, int], user_name: str):
        try:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break
                if data in ['quit', 'exit']:
                    print('{} send the exit request.'.format(user_name))
                    break
                if '=>' in data:
                    try:
                        send_to_name, message = data.split('=>', 1)
                        send_to_name = send_to_name.strip().lower()
                        message = message.strip()
                        if send_to_name == user_name:
                            conn.sendall('Your not able to send to yourself\n'.encode())
                            continue
                        recipient = self.clients.get(send_to_name)
                        if recipient and 'conn' in recipient:
                            recipient['conn'].sendall("{}, {}\n".format(user_name, message).encode())
                        else:
                            conn.sendall("User '{}' not found.\n".format(send_to_name).encode())
                    except ValueError:
                        conn.sendall(b"Invalid message format. Use format: recipient => message\n")
                else:
                    print(data)
        except Exception as e:
            print('Connection closed with {}'.format(user_name))
        finally:
            conn.close()
            self.remove_client_file(user_name)

    def remove_client_file(self, user_name: str):
    # Read current clients from file
        clients = self.read_user_file()
        
        # Remove all entries for this user
        updated_clients = [client for client in clients if user_name not in client]
        
        # Write back to file if changes were made
        if len(updated_clients) != len(clients):
            with open(self.user_file_path, 'w') as file_obj:
                json.dump(updated_clients, file_obj)
            
        # Also remove from in-memory clients if it exists there
        if hasattr(self, 'clients') and user_name in self.clients:
            del self.clients[user_name]
            
    def read_user_file(self) -> list[dict]:
        try:
            with open(self.user_file_path) as file_obj:
                data = json.load(file_obj)
                return data
        except (JSONDecodeError, FileNotFoundError):
            data = []
            return data

    def add_client_to_file(self, client_data: list[dict]):
        data = self.read_user_file()
        data.append(client_data)
        with open(self.user_file_path, 'w') as file_obj:
            json.dump(data, file_obj, indent=4)
    
    def accept_client(self):
        try:
            while True:
                try:
                    self.sock.settimeout(1.0)
                    conn, addr = self.sock.accept()
                except TimeoutError:
                    continue
                #Send the headmessage
                conn.sendall('Welcome to chat server'.encode())
                # Read the username
                name = conn.recv(1024).decode().strip()
                if name:
                    user_name = name
                
                # Store the client data
                client_data = {
                    user_name: {
                        'ip_addr': addr[0],
                        'port': addr[1],
                    }
                }
                self.clients[user_name] = {
                    "conn": conn,
                }
                self.add_client_to_file(client_data)
                print("{} is connected.".format(user_name))
                thread = Thread(target=self.print_receive_data, args=(conn, addr, user_name), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
        except Exception as e:
            print(f"\n[!] Server error: {e}")
        finally:
            # Properly close all client connections
            for client_name, client_info in list(self.clients.items()):
                try:
                    if 'conn' in client_info:
                        client_info['conn'].close()
                except:
                    pass
                self.remove_client_file(client_name)
            if self.sock:
                self.sock.close()

    def run(self):
        self.server()
        self.accept_client()
