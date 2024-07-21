import socket

from ._base_event import Event


class OnTCPServerStart(Event): ...


class OnTCPConnect(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the new socket of type socket.socket as argument"""
        return super().register(func)

    def trigger(self, new_socket) -> None:
        self._call_listeners(new_socket)


class OnTCPPacketReceived(Event):
    def trigger(self, packet):
        self._call_listeners(packet)


class OnTCPDisconnect(Event):
    def trigger(self, remote_socket) -> None:
        self._call_listeners(remote_socket)


class OnTCPServerStop(Event): ...


class OnTCPServerError(Event):
    def trigger(self, sock: socket.socket, exception: Exception):
        self._call_listeners(sock, exception)
