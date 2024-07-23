from ._base_event import Event


class OnRemoteClientCreated(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the new created Client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client) -> None:
        self._call_listeners(client)


class OnRemoteClientTCPPacketReceived(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client  of type Client and the packet of type TCPPacket as arguments"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client, packet):
        self._call_listeners(client, packet)


class OnRemoteClientUDPPacketReceived(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client  of type Client and the packet of type TCPPacket as arguments"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client, packet):
        self._call_listeners(client, packet)


class OnRemoteClientConnect(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client of type Client as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client):
        self._call_listeners(client)


class OnRemoteClientDisconnect(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client):
        self._call_listeners(client)


class OnRemoteClientError(Event):
    def trigger(self, client, exception: Exception):
        self._call_listeners(client, exception)
