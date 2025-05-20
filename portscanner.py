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

def runner(scan_type, addr_ip, starting_port = None, ending_port = None, specific_port = None ):
    if scan_type == 1:
        open_ports = [] 
        try:
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(scan, addr_ip, port) for port in range(0, 65535)]
                for future in futures:
                    result = future.result()
                    if result:
                        open_ports.append(result)
            return open_ports
        except KeyboardInterrupt:
            print('Program exiting........')
            return
    
    #Target port scan
    elif scan_type == 2:
        open_ports = []
        try:
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(scan, addr_ip, port) for port in range(starting_port, ending_port + 1)]
                for future in futures:
                    result = future.result()
                    if result:
                        open_ports.append(result)
            return open_ports
        except KeyboardInterrupt:
            print('Program exiting........')
            return
    
    elif scan_type == 3:
        open_ports = []
        try:
            with ThreadPoolExecutor(max_workers=len(specific_port)) as executor:
                futures = [executor.submit(scan, addr_ip, port) for port in specific_port]
                for future in futures:
                    result = future.result()
                    if result:
                        open_ports.append(result)
            return open_ports
        except KeyboardInterrupt:
            print('Program exiting........')
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

def get_valid_specific_port(prompt):
    while True:
        try:
            ports_string = input(prompt)
            ports = list(map(int, ports_string.split()))
            for port in ports:
                if 0 > port > 65535:
                    ports.remove(port)
                    print("{} Port only should 0 to 65535".format(port))
            return ports
        except ValueError:
            print('Invalid input please enter a valid input')

def scan_types_list():
    print("Scan type " + ':' * 20)
    print("1) AUTO SCAN\n2) TARGET PORT SCAN\n3) SPECIFIC PORT")

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
    
    #Scan types
    scan_types_list()

    try:
        scan_type = int(input('Select any scan type (ex: 1): '))
    except ValueError:
        print('Wrong selection')
        return
    
    if not scan_type:
        return
    if scan_type == 1:
        results = runner(scan_type, addr_ip)
        for result in results:
            print('[OPEN] port {}'.format(result))
        return
    elif scan_type == 2:
        starting_port = get_valid_port('Enter the starting port no, EX(1) : ' )
        ending_port = get_valid_port('Enter the ending port no, EX(300) : ' )

        results = runner(scan_type, addr_ip, starting_port, ending_port)
        for result in results:
            print('[OPEN] port {}'.format(result))
        return
    elif scan_type == 3:
        ports = get_valid_specific_port('Enter the ports (EX: 22 80 443) : ')
        results = runner(scan_type, addr_ip, specific_port=ports)
        for result in results:
            print('[OPEN] port {}'.format(result))
        return
    else:
        print("Bad scan Type.")
        return


if __name__ == '__main__':
    display()
    sys.exit()
