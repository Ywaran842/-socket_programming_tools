import socket as s
from sys import argv, stdin
from threading import Thread

class PrintReceivedData(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def run(self):
        try:
            while True:
                data = self.conn.recv(1024).decode()
                if not data:
                    break
                print('Server =>', data)
        except Exception as e:
            print('Error:', e)
        finally:
            self.conn.close()

def main():
    if len(argv) < 3:
        print("Usage: python3 client.py <IP> <PORT>")
        return

    ip = argv[1]
    port = int(argv[2])

    try:
        soc = s.socket(s.AF_INET, s.SOCK_STREAM)
        soc.connect((ip, port))
        print(f"[+] Connected to {ip}:{port}")

        thread = PrintReceivedData(soc)
        thread.daemon = True
        thread.start()

        while True:
            data = input("You: ").strip()
            if data.lower() in ['exit', 'quit']:
                soc.sendall(data.encode())
                print("[!] Exiting...")
                break
            soc.sendall(data.encode())

    except ConnectionRefusedError:
        print("[!] Server is not running or refused the connection.")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        soc.close()

if __name__ == "__main__":
    main()