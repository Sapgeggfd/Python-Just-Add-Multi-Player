import socket
import threading

from ...enums.tcp_enums import TCPPayloadType
from ...events import (
    on_tcp_client_created,
    on_tcp_client_disconnect,
    on_tcp_client_error,
    on_tcp_client_packet_received,
)
from ...packets.tcp_packet import TCPPacket
from ...utils.static_settings import TCP_HEADER_SIZE


class TCPClient:
    """The TCP Client handles Packets which send offer its tcp_socket"""

    def __init__(self, sock: socket.socket) -> None:
        self.tcp_sock: socket.socket = sock
        threading.Thread(target=self._handle_packets).start()
        on_tcp_client_created.trigger(client=self)

    def _handle_packets(self) -> None:
        """Handles the incoming packets from the clients socket and triggers the event on_tcp_client_packet_received with itself and the packet of type TCPPacket as argument"""
        with self.tcp_sock as sock:
            while self.running:
                try:
                    payload_size: str = sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8")
                    if payload_size.isdecimal():
                        payload: bytes = sock.recv(int(payload_size))
                        packet: TCPPacket = TCPPacket.load(payload=payload)
                        on_tcp_client_packet_received.trigger(client=self, packet=packet)
                except (EOFError, ConnectionResetError) as e:
                    on_tcp_client_error.trigger(exception=e)

    @on_tcp_client_packet_received.register()
    def disconnect_client(self, _=None, packet: TCPPacket = TCPPacket(type=TCPPayloadType.DISCONNECT, data={})):
        """Disconnects this TCPClient from the Server"""
        if packet.type == TCPPayloadType.DISCONNECT:
            on_tcp_client_disconnect.trigger(client=self)

    @on_tcp_client_error.register()
    def _handle_client_error(self, _client, exception) -> None:
        """disconnects the tcp socket on error"""
        self.tcp_sock.close()
        print(exception)
        on_tcp_client_disconnect.trigger(client=self)
