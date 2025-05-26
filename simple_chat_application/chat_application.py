import socket as s
from threading import Thread
import sys
import pyfiglet
from server_socket import ServerSock
import argparse
import json
from json import JSONDecodeError
from pathlib import Path
from client_socket import ClientSock


HOST = ''
PORT = 7645
clients_file_path = Path.cwd() / 'clients.json'
#Banner
def chat_banner(Name: str):
    banner_title = pyfiglet.figlet_format(Name, font="small")
    print(banner_title) # Check running flag

def arg_var()-> argparse.Namespace:
    parser = argparse.ArgumentParser(description = 'Cli Based chat application')
    parser.add_argument("-H", "--host", default='127.0.0.1', help="Adress for the application, Default is 127.0.0.1")
    parser.add_argument("-P", "--port", required=True, type=int, help="Port number")
    parser.add_argument("-T", "--type", required=True, help="Application type to start")
    parser.add_argument("-N", "--name", help="Name of the user")
    arg = parser.parse_args()

    if arg.type == 'client' and not arg.name:
        parser.error('-N , --name required for client')
    return arg

def read_client_file()-> list[dict] | None:
    with open(clients_file_path) as file_obj:
            clients = json.load(file_obj)
            return clients

def check_username(name: str) -> bool:
    try:
        clients = read_client_file()    
            # Iterate through each client dictionary in the list
        for client_dict in clients:
            # Check if the name exists as a key in the current dictionary
            if name in client_dict:
                return True
        return False
            
    except JSONDecodeError as e:
        return False
    except FileNotFoundError:
        print(f"File not found: {clients_file_path}")
        return False

if __name__ == '__main__':
    args = arg_var()

    #check the application type
    if args.type == 'server':
        try:
            #server title banner
            chat_banner('Server_APP_starts')
            print('-'*75)
            sock = ServerSock(args.host, args.port, s, clients_file_path)
            sock.daemon = True  # Make server thread a daemon
            sock.start()
            while sock.is_alive():
                sock.join(timeout=1)  # Join with timeout to allow KeyboardInterrupt
        except KeyboardInterrupt:
            clients = read_client_file()
            clients.clear() 
            with open(clients_file_path, 'w') as file_obj:
                json.dump(clients, file_obj)
            print("Server interrupted. Shutting down...")     
        finally:
            sys.exit()

    if args.type == 'client':
        #check the username is exist
        if check_username(args.name):
            print('User name {} already exist'.format(args.name))
            sys.exit()
        try:
            #Client socket banner
            chat_banner('Client_APP_starts')
            print('-'*50)
            sock = ClientSock(args.name, s, args.host, args.port)
            sock.daemon = True
            sock.start()
            while sock.is_alive():
                sock.join(timeout=1)  # Join with timeout to allow KeyboardInterrupt
        except KeyboardInterrupt:
            print("Server interrupted. Shutting down...")
        finally:
            sys.exit()



