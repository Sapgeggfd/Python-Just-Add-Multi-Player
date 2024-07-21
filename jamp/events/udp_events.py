from ._base_event import Event


class OnUDPServerStart(Event): ...


class OnUDPPacketReceived(Event):
    def trigger(self, packet, remote_addr) -> None:
        self._call_listeners(packet, remote_addr)


class OnUDPServerStop(Event): ...
