from typing import override

from ..enums.tcp_enums import TCPPayloadType
from ..packets.tcp_packet import TCPPacket
from .base_event import Event


class ClientEvent(Event):
    def trigger(self, client):
        for listener in self.__listeners:
            listener(client)


class PacketReceivedEvent(Event):
    def register(self, func=None, *, packet_type: TCPPayloadType = None):
        if func == None:
            return lambda f: self.register(f)
        if packet_type != None:
            self._register_listener(func, packet_type)

    def _register_listener(self, func, packet_type):
        if func not in self.__listeners:
            self.__listeners.append((func, packet_type))

    def unregister_listeners(self, listener: "function"):
        try:
            for li, pt in self.__listeners:
                if li == listener:
                    self.__listeners.remove(listener, pt)
                    break
        except ValueError:
            pass

    def trigger(self, client, packet: TCPPacket):
        for listener in self.__listeners:
            if listener[1] == packet.type:
                listener(client, packet)


on_client_connect = ClientEvent("on_client_connect")
on_client_disconnect = ClientEvent("on_client_disconnect")
on_tcp_packet_received = PacketReceivedEvent("on_packet_received")

on_udp_packet_received = None
