import socket
import uuid
from enum import Enum

from ..enums.tcp_enums import TCPPayloadType
from ..packets.tcp_packet import TCPPacket
from ..packets.UDP_packet import UDPPacket


class Client:
    def __init__(self, uuid: uuid.uuid4) -> None:
        self.client_uuid: uuid.uuid4 = uuid
        self.connected: bool = False
        self.tcp_sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.udp_server_addr: tuple[str, int] = None

    def connect_to_server(self, server_addr: str, port: int):
        self.tcp_sock.connect((server_addr, port))

        connect_packet = TCPPacket(TCPPayloadType.CONNECT, data={"client_uuid": self.client_uuid})
        self.tcp_sock.sendall(connect_packet.dump())

    def send_tcp(self, tcp_type: Enum, payload: dict):
        self.tcp_sock.sendall(TCPPacket(type=tcp_type, data=payload).dump())

    def send_udp(self, udp_type: Enum, payload: dict):
        self.udp_sock.sendto(UDPPacket(type=udp_type, data=payload).dump(), self.udp_server_addr)
