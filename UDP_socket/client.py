import socket as s
from sys import argv
from threading import Thread

class PrintReceivedData(Thread):
    def __init__(self, sock, server_addr):
        super().__init__()
        self.sock = sock
        self.server_addr = server_addr

    def run(self):
        try:
            while True:
                data, _ = self.sock.recvfrom(1024)
                if not data:
                    break
                print('Server => {}'.format(data.decode()))
        except Exception as e:
            print('Error: {}'.format(e))

def main():
    if len(argv) < 3:
        print("Usage: python3 client.py <IP> <PORT>")
        return

    ip = argv[1]
    port = int(argv[2])
    server_addr = (ip, port)

    try:
        sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
        print("[+] Ready to send messages to {}:{}".format(ip, port))

        thread = PrintReceivedData(sock, server_addr)
        thread.daemon = True
        thread.start()

        while True:
            data = input("You: ").strip()
            sock.sendto(data.encode(), server_addr)
            if data.lower() in ['exit', 'quit']:
                print("[!] Exiting...")
                break

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
