from ._base_event import Event


class OnUDPServerStart(Event): ...


class OnUDPPacketReceived(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the packet of type UDPPacket and the remote_addr of the socket as arguments"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, packet, remote_addr) -> None:
        self._call_listeners(packet, remote_addr)


class OnUDPServerStop(Event): ...
