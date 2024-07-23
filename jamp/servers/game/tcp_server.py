import socket

from ...events import (
    on_client_disconnect,
    on_tcp_packet_received,
    on_tcp_server_connect,
    on_tcp_server_disconnect,
    on_tcp_server_error,
    on_tcp_server_start,
    on_tcp_server_stop,
)
from ...packets.tcp_packet import TCPPacket
from ...utils.static_settings import TCP_HEADER_SIZE
from .client import Client


class TCPServer:
    """The TCP Server which is responsible for accepting new connection and handle incoming packages"""

    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port

        self.running = False

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.register_funcs()

    def register_funcs(self):
        on_tcp_server_start.register(self._accept_connections)
        # on_tcp_server_connect.register(self._handle_packet, threaded=True)
        on_tcp_server_connect.register(self._generate_new_client)
        on_tcp_server_error.register(self._tcp_server_error_handler)
        on_client_disconnect.register(self.disconnect_client)

    def start(self) -> None:
        """sets self.running to True and triggers the event on_tcp_server_start with no arguments"""
        self.running = True
        on_tcp_server_start.trigger()

    def stop(self) -> None:
        """sets self.running to False and triggers the event on_tcp_server_stop with no arguments"""
        self.running = False
        on_tcp_server_stop.trigger(tcp_serve=self)

    def _accept_connections(self) -> None:
        """accepts new connections and triggers the event on_tcp_connect with the new Socket as argument"""
        self.tcp_sock.bind((self.host, self.port))
        with self.tcp_sock as sock:
            sock.listen()
            while self.running:
                new_sock, _ = sock.accept()
                on_tcp_server_connect.trigger(new_socket=new_sock)

    def _handle_packet(self, new_sock: socket.socket) -> None:
        """gets new packets that are received from the TCP Socket and triggers the event on_tcp_packet_received with the received packet as argument

        Args:
            new_sock (socket.socket): the socket from the event on_tcp_connect
        """
        while self.running:
            try:
                payload_size: str = new_sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8").strip(" ")
                if payload_size.isdecimal():
                    payload: bytes = new_sock.recv(int(payload_size))
                    packet: TCPPacket = TCPPacket.load(payload=payload)
                    on_tcp_packet_received.trigger(packet=packet)
            except (EOFError, ConnectionResetError) as e:
                on_tcp_server_error.trigger(exception=e)

    def _generate_new_client(self, new_sock: socket.socket) -> None:
        """Generate a new TCPClient"""
        new_client = Client(tcp_sock=new_sock)
        # print(new_client)
        # No trigger because it gets trigger in the init of the TCPClient

    def _tcp_server_error_handler(self, sock: socket.socket, exception: Exception) -> None:
        """closes the TCP Connection on error"""
        sock.close()
        print(exception)
        on_tcp_server_disconnect.trigger(remote_socket=sock, tcp_server=self)

    def disconnect_client(self, client: Client) -> None:
        """Disconnects a tcp_socket and triggers the on_tcp_disconnect.trigger with the remote socket as argument"""
        client_sock = client.tcp_sock
        client_sock.close()
        on_tcp_server_disconnect.trigger(remote_socket=client_sock)
