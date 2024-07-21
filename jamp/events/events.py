import socket
import threading


class _Listener:
    def __init__(self, func: callable, threaded: bool = False, daemon_thread: bool = False) -> None:
        self.func: callable = func
        self.threaded: bool = threaded
        self.daemon_thread = daemon_thread

    def call(self, *args, **kwargs):
        if self.threaded:
            threading.Thread(target=self.func, args=(args, kwargs), daemon=self.daemon_thread).start()
        else:
            self.func(*args, **kwargs)


# Base Event
class Event:
    def __init__(self) -> None:
        self.__listeners: list[_Listener] = []

    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        if func == None:
            return lambda f: self.register(f)
        new_listener = _Listener(func=func, threaded=threaded, daemon_thread=daemon_thread)
        self._register_listener(new_listener)

    def trigger(self, *args, **kwargs) -> None: ...

    def _register_listener(self, listener: _Listener):
        if listener not in self.__listeners:
            self.__listeners.append(listener)

    def _call_listeners(self, *args, **kwargs) -> None:
        for listener in self.__listeners:
            listener.call(*args, **kwargs)


# TCP
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


on_tcp_server_start = OnTCPServerStart()
on_tcp_server_connect = OnTCPConnect()
on_tcp_packet_received = OnTCPPacketReceived()
on_tcp_server_disconnect = OnTCPDisconnect()
on_tcp_server_stop = OnTCPServerStop()
on_tcp_server_error = OnTCPServerError()


# UDP
class OnUDPServerStart(Event): ...


class OnUDPPacketReceived(Event):
    def trigger(self, packet, remote_addr) -> None:
        self._call_listeners(packet, remote_addr)


class OnUDPServerStop(Event): ...


on_udp_server_start = OnUDPServerStart()
on_udp_packet_received = OnUDPPacketReceived()
on_udp_server_stop = OnUDPServerStop()


# TCP Client
class OnTCPClientCreated(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the new created TCP client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client) -> None:
        self._call_listeners(client)


class OnTCPClientPacketReceived(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client  of type TCPClient and the packet of type TCPPacket as arguments"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client, packet):
        self._call_listeners(client, packet)


class OnTCPClientDisconnect(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """on trigger it parses the client of type TCPClient as argument"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)

    def trigger(self, client):
        self._call_listeners(client)


class OnTCPClientError(Event):
    def trigger(self, client, exception: Exception):
        self._call_listeners(client, exception)


on_tcp_client_created = OnTCPClientCreated()
on_tcp_client_packet_received = OnTCPClientPacketReceived()
on_tcp_client_disconnect = OnTCPClientDisconnect()
on_tcp_client_error = OnTCPClientError()
