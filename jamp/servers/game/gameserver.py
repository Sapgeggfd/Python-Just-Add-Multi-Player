import uuid

from ...events import *
from .tcp_server import TCPServer
from .udp_server import UDPServer


class GameServer:
    def __init__(self) -> None:
        self.running: bool = False
        self.uuid: uuid.uuid4 = uuid.uuid4()

        # Network
        self.hostname: str = "localhost"
        self.tcp_port: int = 5555
        self.udp_port: int = 5556

        # Server
        self.tcp_server = TCPServer(host=self.hostname, port=self.tcp_port)
        self.udp_server = UDPServer(host=self.hostname, port=self.udp_port)

        # Clients
        self.__clients: list = []
        self.max_clients: int = 20

    def _register_funcs(self):
        on_udp_packet_received.register(self._dispatch_udp_packet, threaded=True)
        on_client_created.register(self.add_client)

    @property
    def clients(self) -> list:
        return self.__clients

    def _start_tcp_server(self) -> None:
        self.tcp_server.start()

    def _start_udp_server(self) -> None:
        self.udp_server.start()

    def _dispatch_udp_packet(self, packet, remote_addr):
        for client in self.__clients:
            if client.remote_addr == remote_addr:
                client.udp_queue.add(packet)

    def add_client(self, new_client=None):
        if new_client not in self.__clients:
            self.__clients.append(new_client)

    def start(self):
        self.running = True
        self._start_tcp_server()
        self._start_udp_server()
        on_gameserver_start.trigger()

    def stop(self):
        self.running = False
        self.tcp_server.stop()
        self.udp_server.stop()
        on_gameserver_stop.trigger()
