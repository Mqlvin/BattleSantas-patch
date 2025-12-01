import socket
import threading
from edit_me import SERVER_HOST, SERVER_PORT, handshake, take_turn

def recv_server(conn):
    while True:
        message = conn.recv(1024)
        if message:
            print(message.decode())

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = internet protocol
    sock.connect((SERVER_HOST, SERVER_PORT))
    sock.send(Packet("HANDSHAKE", handshake()).get_bytes())
    while True:
        packet = sock.recv(1024)
        if packet:
            print(packet)
    sock.close()

if __name__ == "__main__":
    main()

