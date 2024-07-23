from ._base_event import Event


class OnClientCreated(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the new created TCP client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client) -> None:
        self._call_listeners(client)


class OnClientTCPPacketReceived(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client  of type TCPClient and the packet of type TCPPacket as arguments"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client, packet):
        self._call_listeners(client, packet)


class OnClientConnect(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client):
        self._call_listeners(client)


class OnClientDisconnect(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client):
        self._call_listeners(client)


class OnClientError(Event):
    def trigger(self, client, exception: Exception):
        self._call_listeners(client, exception)
