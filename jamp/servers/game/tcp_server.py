import socket

from ...events.events import (
    on_tcp_client_disconnect,
    on_tcp_packet_received,
    on_tcp_server_connect,
    on_tcp_server_disconnect,
    on_tcp_server_error,
    on_tcp_server_start,
    on_tcp_server_stop,
)
from ...packets.tcp_packet import TCPPacket
from ...utils.static_settings import TCP_HEADER_SIZE
from .tcp_client import TCPClient


class TCPServer:
    """The TCP Server which is responsible for accepting new connection and handle incoming packages"""

    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port

        self.running = False

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self) -> None:
        """sets self.running to True and triggers the event on_tcp_server_start with no arguments"""
        self.running = True
        on_tcp_server_start.trigger()

    def stop(self) -> None:
        """sets self.running to False and triggers the event on_tcp_server_stop with no arguments"""
        self.running = False
        on_tcp_server_stop.trigger()

    @on_tcp_server_start.register()
    def _accept_connections(self) -> None:
        """accepts new connections and triggers the event on_tcp_connect with the new Socket as argument"""
        self.tcp_sock.bind((self.host, self.port))
        with self.tcp_sock as sock:
            sock.listen()
            while self.running:
                new_sock, _ = sock.accept()
                on_tcp_server_connect.trigger(new_socket=new_sock)

    @on_tcp_server_connect.register(threaded=True)
    def _handle_packet(self, new_sock: socket.socket) -> None:
        """gets new packets that are received from the TCP Socket and triggers the event on_tcp_packet_received with the received packet as argument

        Args:
            new_sock (socket.socket): the socket from the event on_tcp_connect
        """
        with new_sock as sock:
            while self.running:
                try:
                    payload_size: str = sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8")
                    if payload_size.isdecimal():
                        payload: bytes = sock.recv(int(payload_size))
                        packet: TCPPacket = TCPPacket.load(payload=payload)
                        on_tcp_packet_received.trigger(packet=packet)
                except (EOFError, ConnectionResetError) as e:
                    on_tcp_server_error.trigger(exception=e)

    @on_tcp_server_connect.register()
    def _generate_new_client(self, new_sock: socket.socket) -> None:
        """Generate a new TCPClient"""
        new_client = TCPClient(sock=new_sock)
        # No trigger because it gets trigger in the init of the TCPClient

    @on_tcp_server_error.register
    def _tcp_server_error_handler(self, sock: socket.socket, exception: Exception) -> None:
        """closes the TCP Connection on error"""
        sock.close()
        print(exception)
        on_tcp_server_disconnect.trigger(remote_socket=sock)

    @on_tcp_client_disconnect.register()
    def disconnect_client(self, client: TCPClient) -> None:
        """Disconnects a tcp_socket and triggers the on_tcp_disconnect.trigger with the remote socket as argument"""
        client_sock = client.tcp_sock
        client_sock.close()
        on_tcp_server_disconnect.trigger(remote_socket=client_sock)
