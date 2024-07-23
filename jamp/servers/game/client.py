import queue
import socket
import threading
import uuid
from enum import Enum

from ...enums.tcp_enums import TCPPayloadType
from ...events import (
    on_client_connected,
    on_client_created,
    on_client_disconnect,
    on_client_error,
    on_client_tcp_packet_received,
    on_client_udp_packet_received,
)
from ...packets.tcp_packet import TCPPacket
from ...packets.UDP_packet import UDPPacket
from ...utils.static_settings import TCP_HEADER_SIZE


class Client:
    """The TCP Client handles Packets which send offer its tcp_socket"""

    def __init__(self, tcp_sock: socket.socket) -> None:
        self.client_uuid: uuid.uuid4 = None
        self.running = True

        self.tcp_sock: socket.socket = tcp_sock
        self.remote_addr = self.tcp_sock.getpeername()

        self.udp_sock: socket.socket = None

        self._udp_queue = queue.Queue()

        threading.Thread(target=self._handle_packets).start()
        on_client_created.trigger(client=self)
        self._register_funcs()

    def add_udp_queue(self, new_packet: UDPPacket):
        self._udp_queue.put(new_packet)
        on_client_udp_packet_received.trigger(client=self, packet=new_packet)

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
            except (EOFError, ConnectionResetError, ConnectionAbortedError) as e:
                on_client_error.trigger(client=self, exception=e)

    def connect_client(self, _=None, packet: TCPPacket = None):
        """First TCP data to set the client uuid"""
        if packet.type == TCPPayloadType.CONNECT:
            self.client_uuid = packet.data.get("client_uuid")
            on_client_connected.trigger(client=self)

    def disconnect_client(self, _=None, packet: TCPPacket = TCPPacket(type=TCPPayloadType.DISCONNECT, data={})):
        """Disconnects this TCPClient from the Server"""
        if packet.type == TCPPayloadType.DISCONNECT:
            on_client_disconnect.trigger(client=self)

    def _handle_client_error(self, _client, exception) -> None:
        """disconnects the tcp socket on error"""
        self.running = False
        self.tcp_sock.close()
        print(exception)
        on_client_disconnect.trigger(client=self)

    def send_tcp(self, tcp_type: Enum, payload: dict):
        self.tcp_sock.sendall(TCPPacket(type=tcp_type, data=payload).dump())

    def send_udp(self, udp_type: Enum, payload: dict):
        self.udp_sock.sendto(UDPPacket(type=udp_type, data=payload).dump(), self.remote_addr)
