import pyfiglet
import sys
import socket as s
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

 
def scan(addr_ip, addr_port):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    #scan the port
    result = sock.connect_ex((addr_ip, addr_port))
    #check if port is open or not
    if result == 0:
        return addr_port

def runner(scan_type, addr_ip, starting_port = None, ending_port = None):
    if scan_type == 1:
        try:
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(scan, addr_ip, port) for port in range(0, 65535)]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        print('[OPEN] port {}'.format(result))
        except KeyboardInterrupt:
            print('Program exiting........')
            return
        finally:
            return
    
    #Target port scan
    elif scan_type == 2:
        try:
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(scan, addr_ip, port) for port in range(starting_port, ending_port)]
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        print('[OPEN] port {}'.format(result))
        except KeyboardInterrupt:
            print('Program exiting........')
            return
        finally:
            return


def get_port(prompt):
    while True:
        try:
            port = int(input(prompt))
            if 0 <= port <= 65535:
                return port
            else:
                print('Port must be between 0 to 65535')
        except ValueError:
            print('Invalid input please enter a valid input')

def banner():
    banner_title = pyfiglet.figlet_format("PORT SCANNER")
    print(banner_title)

def display():
    banner()
    print('-' * 70)
    #Get the addr_ip
    addr_ip = input("Enter the target ip address : ")
    if not addr_ip:
        print("Target ip is empty")
        return
    print("Scan type " + ':' * 20)
    print("1) AUTO SCAN\n2) TARGET PORT SCAN")
    scan_type = int(input('Select any scan type (ex: 1): '))
    if not scan_type:
        return
    if scan_type == 1:
        runner(scan_type, addr_ip)
        return
    elif scan_type == 2:
        starting_port = int(input('Enter the starting port ex(1): '))
        if not starting_port:
            print('Starting port is not metioned')
            starting_port = int(input('Enter the starting port ex(1): '))

        runner(scan_type, starting_port, ending_port)
        return



if __name__ == '__main__':
    display()
    sys.exit()
