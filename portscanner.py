import pyfiglet
import sys
import socket as s
from datetime import datetime
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

 
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

def is_valid_ipv4(ip):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, ip):
        parts = ip.split(".")
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def get_valid_port(prompt):
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
    if not is_valid_ipv4(addr_ip):
        print("Target ip is wrong")
        return
    print("Scan type " + ':' * 20)
    print("1) AUTO SCAN\n2) TARGET PORT SCAN")
    scan_type = int(input('Select any scan type (ex: 1): '))
    print('\n')
    if not scan_type:
        return
    if scan_type == 1:
        runner(scan_type, addr_ip)
        return
    elif scan_type == 2:
        starting_port = get_valid_port('Enter the starting port no, EX(1) : ' )
        ending_port = get_valid_port('Enter the ending port no, EX(300) : ' )

        runner(scan_type, addr_ip, starting_port, ending_port)
        return



if __name__ == '__main__':
    display()
    sys.exit()
