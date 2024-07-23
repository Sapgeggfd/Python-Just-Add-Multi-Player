import socket
from typing import Protocol

from ...utils.static_settings import *


class GameServer(Protocol): ...


class UDPServer:
    host: str
    port: int
    game_server: GameServer

    def __init__(self, host: str, port: int, game_server: GameServer) -> None:
        self.host = host
        self.port = port
        self.game_server = game_server

        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self) -> None:

        with self.udp_sock as sock:
            sock.bind((self.host, self.port))
            try:
                data, client_addr = sock.recvfrom(UDP_PACKET_SIZE)

            except Exception as e:
                print(e)

    def stop(self): ...
