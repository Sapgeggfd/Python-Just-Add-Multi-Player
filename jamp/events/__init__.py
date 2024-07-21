from ._base_event import Event
from .tcp_client_events import *
from .tcp_events import *
from .udp_events import *

# TCP Events
on_tcp_server_start = OnTCPServerStart()
on_tcp_server_connect = OnTCPConnect()
on_tcp_packet_received = OnTCPPacketReceived()
on_tcp_server_disconnect = OnTCPDisconnect()
on_tcp_server_stop = OnTCPServerStop()
on_tcp_server_error = OnTCPServerError()

# UDD Events
on_udp_server_start = OnUDPServerStart()
on_udp_packet_received = OnUDPPacketReceived()
on_udp_server_stop = OnUDPServerStop()


# TCP Client
on_tcp_client_created = OnTCPClientCreated()
on_tcp_client_packet_received = OnTCPClientPacketReceived()
on_tcp_client_disconnect = OnTCPClientDisconnect()
on_tcp_client_error = OnTCPClientError()
