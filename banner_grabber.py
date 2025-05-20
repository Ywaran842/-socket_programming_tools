from portscanner import is_valid_ipv4, get_valid_port, get_valid_specific_port, scan_types_list, runner
import pyfiglet
import sys
import socket as s
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner():
    banner_title = pyfiglet.figlet_format("BANNER GRABBER", font="small")
    print(banner_title)

def banner_scan(addr_ip, port):
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((addr_ip, port))
        sock.send(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        banner = sock.recv(4096).decode(errors='ignore').strip()
        sock.close()

        try:
            service = s.getservbyport(port, 'tcp')
        except OSError:
            service = "unknown"

        version_info = "unknown"

        if service == 'http' or banner.upper().startswith("HTTP"):
            # Parse HTTP headers line by line to find Server header
            lines = banner.split('\n')
            server_header = None
            for line in lines:
                if line.lower().startswith('server:'):
                    server_header = line.strip()
                    break
            if server_header:
                version_info = server_header
            else:
                version_info = banner.split('\n')[0]  # fallback to first line
        elif service == 'ssh' and banner.lower().startswith("ssh-"):
            version_info = banner.split('\n')[0]
        else:
            version_info = banner.split('\n')[0] if banner else "unknown"

        return {
            "port": port,
            "state": "open",
            "service": service,
            "version": version_info
        }

    except:
        return None

def banner_runner(addr_ip, Specific_ports=None):
    try:
        print(f"{'PORT':<8} {'STATE':<6} {'SERVICE':<8} {'VERSION'}")
        print("-" * 60)
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(banner_scan, addr_ip, port) for port in Specific_ports]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    port_str = f"{result['port']}/tcp"
                    print(f"{port_str:<8} {result['state']:<6} {result['service']:<8} {result['version']}")
    except KeyboardInterrupt:
        print('Program exiting........')
        return

def display():
    banner()
    print('-'*75)

    #Get the ip address
    addr_ip = input("Enter the target ip address : ")
    if not is_valid_ipv4(addr_ip):
        print("Target ip is wrong")
        return
    
    #Scan type
    scan_types_list()

    try:
        scan_type = int(input('Select any scan type (ex: 1): '))
        print("\n")
    except ValueError:
        print('Wrong selection')
        return
    
    if not scan_type:
        return
    if scan_type == 1:
        #Scan the open ports
        open_ports = runner(scan_type = scan_type, addr_ip=addr_ip)
        if not open_ports is None:
            banner_runner(addr_ip=addr_ip,Specific_ports=open_ports)
        else:
            print("None of the port is open in this ip {}".format(addr_ip))
        return
    elif scan_type == 2:
        starting_port = get_valid_port('Enter the starting port no, EX(1) : ' )
        ending_port = get_valid_port('Enter the ending port no, EX(300) : ' )
        
        #Get the open ports
        open_ports = runner(scan_type=scan_type, addr_ip=addr_ip, starting_port=starting_port, ending_port=ending_port)
        if not open_ports is None:
            banner_runner(addr_ip=addr_ip, Specific_ports=open_ports)
        else:
            print('None of the port from {} to {} is open in this ip {}'.format(starting_port, ending_port, addr_ip))
        return
    elif scan_type == 3:
        ports = get_valid_specific_port('Enter the ports (EX: 22 80 443) : ')
        #Get the open ports
        open_ports = runner(scan_type, addr_ip, specific_port=ports)
        if not open_ports is None:
            banner_runner(addr_ip=addr_ip, Specific_ports=open_ports)
        else:
            print('None of the ports {} open in this ip {}'.format(ports, addr_ip))
        return
    else:
        print("Bad scan type.")
        return
            



if __name__ == '__main__':
    display()
    sys.exit()
