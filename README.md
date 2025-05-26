
# Project Title

Socket programming tool using Python


![Logo](https://academy.selfmade.ninja/assets/brand/logo-text-2.svg)


## Requirements

- Python 3.8+
- `pyfiglet` (for ASCII banners)

Install dependencies:
```bash
pip install pyfiglet
    
## Port scanner
A fast, multi-threaded port scanner written in Python. This tool allows you to scan a target host for open TCP ports using different scanning modes. It uses Python's `ThreadPoolExecutor` for high performance and responsiveness.

Run the Tool
Scan type ::::::::::::::::::::
1) AUTO SCAN
2) TARGET PORT SCAN
3) SPECIFIC PORT

## Banner_grabber
A multi-threaded banner grabbing tool that identifies open ports and grabs service banners from a target host. Useful for service identification, vulnerability assessment, and network reconnaissance.

Scan type ::::::::::::::::::::
1) AUTO SCAN
2) TARGET PORT SCAN
3) SPECIFIC PORT


## TCP_socket_program
A simple TCP client-server chat tool built with Python sockets and threading. This tool demonstrates the basics of TCP communication, allowing a client to connect to a server and exchange messages interactively.

## UDP_socket_programming
A simple UDP client-server messaging tool built with Python sockets and threading. This tool demonstrates the basics of UDP (connectionless) communication, allowing a client to send messages to a server and receive responses in real time.

## cli_chat_application
Simple Chat Application

How to Run

Start the server: python3 chat_application.py -T server -P 7645

Start a client (in another terminal): python3 chat_application.py -T client -P 7645 -N alice

Start more clients with different names: python3 chat_application.py -T client -P 7645 -N bob

How to Use

When prompted, type messages in the client terminal. To send a direct message:
bob => Hello Bob!

To exit, type: exit

Sample Output

Server: Server_APP_starts
alice is connected. bob is connected. alice send the exit request.

Client (alice): Welcome to chat server You: bob => Hi Bob! You: exit [!] Exiting...

Client (bob): Welcome to chat server alice => Hi Bob! You: exit [!] Exiting...