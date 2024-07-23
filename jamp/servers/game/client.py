import queue
import socket
import threading
import uuid

from ...enums.tcp_enums import TCPPayloadType
from ...events import (
    on_client_connected,
    on_client_created,
    on_client_disconnect,
    on_client_error,
    on_client_tcp_packet_received,
)
from ...packets.tcp_packet import TCPPacket
from ...utils.static_settings import TCP_HEADER_SIZE


class Client:
    """The TCP Client handles Packets which send offer its tcp_socket"""

    def __init__(self, sock: socket.socket) -> None:
        self.client_uuid: uuid.uuid4 = None
        self.running = True

        self.tcp_sock: socket.socket = sock
        self.remote_addr = self.tcp_sock.getpeername()

        self.udp_queue = queue.Queue()

        threading.Thread(target=self._handle_packets).start()
        on_client_created.trigger(client=self)
        self._register_funcs()

    def _register_funcs(self):
        on_client_tcp_packet_received.register(self.connect_client)
        on_client_tcp_packet_received.register(self.disconnect_client)
        on_client_error.register(self._handle_client_error)

    def _handle_packets(self) -> None:
        """Handles the incoming packets from the clients socket and triggers the event on_tcp_client_packet_received with itself and the packet of type TCPPacket as argument"""

        while self.running:
            try:
                payload_size: str = self.tcp_sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8").strip(" ")
                if payload_size.isdecimal():
                    payload: bytes = self.tcp_sock.recv(int(payload_size))
                    packet: TCPPacket = TCPPacket.load(payload=payload)
                    on_client_tcp_packet_received.trigger(client=self, packet=packet)
            except (EOFError, ConnectionResetError) as e:
                on_client_error.trigger(exception=e)

    def connect_client(self, _=None, packet: TCPPacket = None):
        """First TCP data to set the client uuid"""
        print(packet.type)
        if packet.type == TCPPayloadType.CONNECT:
            print(packet.data.get("client_uuid").hex)
            self.client_uuid = packet.data.get("client_uuid")
            on_client_connected.trigger(client=self)

    def disconnect_client(self, _=None, packet: TCPPacket = TCPPacket(type=TCPPayloadType.DISCONNECT, data={})):
        """Disconnects this TCPClient from the Server"""
        if packet.type == TCPPayloadType.DISCONNECT:
            on_client_disconnect.trigger(client=self)

    def _handle_client_error(self, _client, exception) -> None:
        """disconnects the tcp socket on error"""
        self.tcp_sock.close()
        print(exception)
        on_client_disconnect.trigger(client=self)
