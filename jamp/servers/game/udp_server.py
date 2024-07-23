import socket
import threading

from ...events import *
from ...packets.UDP_packet import UDPPacket
from ...utils.static_settings import *


class UDPServer:
    host: str
    port: int

    def __init__(self, host: str, port: int) -> None:
        self.running: bool = False

        self.host = host
        self.port = port

        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self) -> None:
        self.running = True
        threading.Thread(target=self._handle_packets)
        on_udp_server_start.trigger()

    def _handle_packets(self):
        while self.running:
            with self.udp_sock as sock:
                sock.bind((self.host, self.port))
                try:
                    data, client_addr = sock.recvfrom(UDP_PACKET_SIZE)
                    packet: UDPPacket = UDPPacket.load(payload=data)
                    on_udp_packet_received.trigger(packet=packet, remote_addr=client_addr)
                except Exception as e:
                    print(e)

    def stop(self):
        self.running = False
        on_udp_server_stop.trigger()
