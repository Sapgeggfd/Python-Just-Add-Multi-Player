import logging
import socket
import threading
from typing import Protocol

from ...packets.tcp_packet import TCPPacket
from ...utils.custom_logger import TCPServerLogger
from .client import Client


class GameServer(Protocol):
    clients = list[Client]

    def add_client(client: Client) -> bool: ...
    def remove_client(client: Client) -> None: ...


class TCPServer:
    logger: logging.Logger

    running: bool
    host: str
    port: int

    custom_client: Client

    tcp_socket: socket.socket

    def __init__(self, host: str, port: int, game_server: GameServer, *, custom_client: Client = Client) -> None:
        self.logger = TCPServerLogger

        self.running = False
        self.host = host
        self.port = port

        self.custom_client = custom_client

        self.game_server = game_server

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self) -> None:
        self.running = True
        with self.tcp_socket as sock:
            sock.bind((self.host, self.port))
            sock.listen()
            self.logger.info(f"Started listening on [{self.host}:{self.port}]")
            while self.running:
                client_sock, addr = sock.accept()
                self.logger.info(f"New Connection from [{addr}]")
                threading.Thread(target=self._client_connect, args=(client_sock, addr)).start()

    def _client_connect(self, client_sock, addr):
        new_client: Client = self.custom_client(address=addr, tcp_sock=client_sock, tcp_server=self)
        if new_client._wait_for_connect():
            if self.game_server.add_client(new_client):
                threading.Thread(target=Client._handle_tcp_connection).start()
                return
        del new_client

    def _clear_up_player(self):
        while self.running:
            dc_clients = []
            for client in self.game_server.clients:
                if client.disconnected:
                    dc_clients.append(client)
            for client in dc_clients:
                self.game_server.remove_client(client)

    def broadcast(self, packet: TCPPacket):
        for client in self.game_server.clients:
            client.send(packet)
