import logging
import threading
import uuid
from typing import Any

import requests

from ...utils.custom_logger import GameServerLogger
from ...utils.static_settings import CERTIFICATE, SERVER_REGISTRATION_SERVER_URL
from .client import Client
from .tcp_server import TCPServer
from .udp_server import UDPServer


class GameServer:

    running: bool
    logger: logging.Logger
    cert: None | str

    # Server Data
    server_id: uuid.uuid4
    server_location: Any

    # Network
    host_name: str
    tcp_port: int | None
    udp_port: int | None

    # Clients
    clients: list
    max_clients: int

    # Util Servers
    registration_server: None | str  # Server ip which is responsive for managing all servers

    custom_tcp_server: TCPServer
    custom_udp_server: UDPServer

    def __init__(
        self,
        host_name: str = "localhost",
        tcp_port: int | None = 5555,
        udp_port: int | None = 5556,
        max_clients: int = 10,
        *,
        custom_tcp_server: TCPServer = TCPServer,
        custom_udp_server: UDPServer = UDPServer,
    ) -> None:
        self.running = False
        self.logger = GameServerLogger
        self.cert = CERTIFICATE

        # Server Data
        self.server_id = uuid.uuid4()

        # Network
        self.host_name = host_name
        self.tcp_port = tcp_port
        self.udp_port = udp_port

        # Clients
        self._clients = []
        self.max_clients = max_clients

        # Util Server
        self.registration_server = SERVER_REGISTRATION_SERVER_URL

        # custom server
        self.custom_tcp_server = custom_tcp_server
        self.custom_udp_server = custom_udp_server

        self.tcp_server = None
        self.udp_server = None

    @property
    def clients(self) -> list[Client]:
        return self._clients

    def add_client(self, client: Client):
        if any(client.user_uuid == user_uuid for user_uuid in self.clients):
            client.disconnect(reason="User with this UUID is already on the Server")  # TODO Better Error handling
            return False
        else:
            self._clients.append(client)
            return True

    def remove_client(self, client: Client):
        try:
            self._clients.remove(client)
        except ValueError:
            pass

    def _register_server(self):
        payload = {
            "server_id": self.server_id.hex,
            "server_host_name": self.host_name,
            "server_tcp_port": self.tcp_port,
            "server_udp_port": self.udp_port,
            "max_clients": self.max_clients,
        }
        self.logger.info(
            f"restarting to Register-Server [{self.registration_server}/register/server] Payload: {payload} "
        )
        try:
            response = requests.post(
                f"{self.registration_server}/register/server", json=payload, cert=self.cert if self.cert else None
            )
        except requests.ConnectionError as e:
            self.logger.warn(f"AUTH FAILED with exception: {e}")
            return False

        if response.status_code == 200:
            self.logger.info(f"Server Successful register")
            return True
        else:
            self.logger.warn(f"AUTH FAILED [{response.status_code}]: {response.content}")

    def start_tcp_server(self):
        self.tcp_server: TCPServer = self.custom_tcp_server(
            host=self.host_name, port=self.tcp_port, game_server=GameServer
        )
        threading.Thread(target=self.tcp_server.run).start()

    def start_udp_server(self):
        self.udp_server: UDPServer = self.custom_udp_server(
            host=self.host_name, port=self.tcp_port, game_server=GameServer
        )
        threading.Thread(target=self.udp_server.run).start()

    def start(self) -> None:
        self.running = True
        self.start_up()

    def start_up(self) -> None:
        self.logger.info("Starting Server")
        if self.registration_server:
            self._register_server()
        self.start_tcp_server()
        # self.start_udp_server()

    def on_ready(self) -> None: ...
    def on_shutdown(self) -> None: ...
