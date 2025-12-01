from common import Game, Direction, SantaID
from edit_me import handshake, take_turn
from threading import Thread, Event
import time
from datetime import datetime

class Packet:
    @staticmethod
    def get_time():
        return datetime.now().strftime("%A %-d %B %Y %H:%M:%S")

    def __init__(self, header: str, data: str, time=get_time()):
        self.__time = time
        self.header = header
        self.data = data

    def __str__(self):
        return f"{self.__time}\n{self.__header}\n{self.__data}"

    @classmethod
    def from_bytes(cls, bytes):
        packet_str = bytes.decode()
        packet_lines = packet_str.split("\n")
        if len(packet_lines) != 3:
            raise ValueError("Bad packet.")
        return cls(*packet_lines)

    def get_bytes(self):
        return str(self).encode()

class Connection:
    def __init__(self, connection, address, running):
        self.__connection = connnection
        self.__address = address
        self.__running_event = running
        self.__name = ""
        self.__direction = None
        self.__thread  = Thread(target=self.__thread_target)
        self.__thread.start()

    def __thread_target(self):
        self.__received_packet.clear()
        while self.__running_event.is_set():
            try:
                data = conn.recv(1024)
                packet = Packet.from_bytes(data)
                if packet.header == "DIRECTION":
                    self.__direction = getattr(Direction, packet.data)
                elif packet.header == "HANDSHAKE":
                    self.__name = packet.data
            except Exception as e:
                print(f"Exception: {e}")
                packet = Packet("EXCEPTION", f"An error occured. Your connection has been terminated. error={type(e)}".encode())
                conn.send(packet.get_bytes())
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
                break

    def get_name(self):
        return self.__name

    def get_direction(self):
        direction = self.__direction
        self.__direction = None
        return direction

    def get_address(self):
        return f"{self.__address[0]}:{self.__address[1]}"

class Server(Game):
    def __init__(self):
        super().__init__()
        self.__accepting_event = Event()
        self.__running_event = Event()
        self.__await_event = Event()
        self.__accepter = Thread(target=self.__accept_target)
        self.__thread = Thread(target=self.__thread_target)
        self.__connections = list()
        self.__direction_dict = dict()
        self.__connection_names = dict()
        self.__host = "0.0.0.0"
        self.__port = 27910

    def __accept_target(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = internet protocol
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.__host, self.__port))
        while self.__running_event.is_set():
            conn, addr = sock.accept()
            if self.__accepting_event.is_set():
                self.__connections.append(Connection(conn, addr))

    def __thread_target(self):
        self.__direction_dict = dict()
        while self.__running_event.is_set():
            if self.__await_event.is_set():
                for connection in self.__connections:
                    direction = connection.get_direction()
                    address = connection.get_address()
                    if direction is not None:
                        self.__direction_dict[address] = direction
                    self.__connection_names[address] = connection.get_name()
                if len(self.__direction_dict) == len(self.__connections):
                    self.__await_event.clear()

    def start_server(self):
        self.__running_event.set()
        self.__accepting_event.set()
        self.__await_event.clear()
        self.__accepter.start()
        self.__thread.start()

    def lock_server(self):
        self.__accepting_event.clear()

    def stop_server(self):
        self.__running_event.clear()
        self.__thread.join()
        self.__accepter.join()

    def get_server_ip(self) -> str:
        return f"{self.__host}:{self.__port}"

    def get_santa_ids(self) -> list[SantaID]:
        santa_ids = list()
        for address, name in self.__connection_names.items():
            santa_ids.append(SantaID(address, name))
        return santa_ids

    def request_santas(self) -> None:
        self.__await_event.set()

    def received_santas(self) -> bool:
        return not self.__await_event.is_set()

    def get_santas(self) -> list[tuple[str, Direction]]:
        return self.__direction_dict.items()

def main():
    game = Server()
    game.run()

if __name__ == "__main__":
    main()
