import socket as s
from threading import Thread
import sys
import pyfiglet
from server_socket import ServerSock
import argparse
import json
from json import JSONDecodeError
from pathlib import Path


HOST = ''
PORT = 7645
clients_file_path = Path.cwd() / 'clients.json'
#Banner
def server_banner(Name: str):
    banner_title = pyfiglet.figlet_format(Name, font="small")
    print(banner_title)

def arg_var()-> argparse.Namespace:
    parser = argparse.ArgumentParser(description = 'Cli Based chat application')
    parser.add_argument("-H", "--host", default='127.0.0.1', help="Adress for the application, Default is 127.0.0.1")
    parser.add_argument("-P", "--port", required=True, type=int, help="Port number")
    parser.add_argument("-T", "--type", required=True, help="Application type to start")
    parser.add_argument("-N", "--name", required=True, help="Name of the user")
    arg = parser.parse_args()
    return arg

def check_username(name: str) -> bool:
    try:
        with open(clients_file_path) as file_obj:
            clients = json.load(file_obj)
            if name in clients:
                return True
            else:
                return False
    except JSONDecodeError as e:
        return False

if __name__ == '__main__':
    args = arg_var()
    #check the username is exist
    if check_username(args.name):
        print('User name {} already exist'.format(args.name))
        sys.exit()

    #check the application type
    if args.type == 'server':
        sock = ServerSock(args.host, args.port, s, args.name.strip().lower(), clients_file_path)
        #Start the server
        sock.start()

    
