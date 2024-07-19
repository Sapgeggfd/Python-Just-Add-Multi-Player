from typing import override

from ..enums.tcp_server_enums import PayloadType
from ..packets.tcp_packet import TCPPacket
from .base_event import Event


class PacketReceivedEvent(Event):
    def register_handler(self, handler: "function", packet_type: PayloadType):
        self.handlers.append((handler, packet_type))

    def trigger(self, packet: TCPPacket, packet_type: PayloadType):
        for handler, pt in self.handlers:
            if pt == packet_type:
                handler(packet)


on_client_connect = Event("on_client_connect")
on_client_disconnect = Event("on_client_disconnect")
on_packet_received = PacketReceivedEvent("on_packet_received")
