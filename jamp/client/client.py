import socket
import threading
import uuid
from enum import Enum

from ..enums.tcp_enums import TCPPayloadType
from ..events import *
from ..packets.tcp_packet import TCPPacket
from ..packets.UDP_packet import UDPPacket
from ..utils.static_settings import *


class Client:
    def __init__(self, uuid: uuid.uuid4) -> None:
        self.client_uuid: uuid.uuid4 = uuid
        self.connected: bool = False
        self.tcp_sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.udp_server_port: int = None

        self.register_funcs()

    def register_funcs(self):
        on_remote_client_tcp_packet_received.register(self._get_remote_server_udp_port)

    def _get_remote_server_udp_port(self, _, packet):
        if packet.type == TCPPayloadType.CONNECT:
            self.udp_server_port = packet.data.get("udp_port")
            self.udp_sock.bind((self.server_ip, self.udp_server_port))
            threading.Thread(target=self._receive_udp_packets, daemon=True).start()

    def connect_to_server(self, server_addr: str, port: int):
        self.server_ip = server_addr
        self.tcp_sock.connect((server_addr, port))

        connect_packet = TCPPacket(TCPPayloadType.CONNECT, data={"client_uuid": self.client_uuid})
        self.tcp_sock.sendall(connect_packet.dump())

        self.connected = True
        threading.Thread(target=self._receive_tcp_packets, daemon=True).start()

    def _receive_tcp_packets(self):
        while self.connected:
            try:
                payload_size: str = self.tcp_sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8").strip(" ")
                if payload_size.isdecimal():
                    payload: bytes = self.tcp_sock.recv(int(payload_size))
                    packet: TCPPacket = TCPPacket.load(payload=payload)
                    on_remote_client_tcp_packet_received.trigger(client=self, packet=packet)
            except (EOFError, ConnectionResetError) as e:
                on_client_error.trigger(client=self, exception=e)

    def _receive_udp_packets(self):
        while self.connected:
            new_data, addr = self.udp_sock.recvfrom(UDP_PACKET_SIZE)
            on_remote_client_udp_packet_received.trigger(client=self, packet=UDPPacket.load(new_data))

    def send_tcp(self, tcp_type: Enum, payload: dict):
        self.tcp_sock.sendall(TCPPacket(type=tcp_type, data=payload).dump())

    def send_udp(self, udp_type: Enum, payload: dict):
        self.udp_sock.sendto(UDPPacket(type=udp_type, data=payload).dump(), (self.server_ip, self.udp_server_port))
