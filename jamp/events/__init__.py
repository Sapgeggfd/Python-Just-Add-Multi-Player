from ._base_event import Event
from .client_events import *
from .gameserver_events import *
from .remote_client_event import *
from .tcp_events import *
from .udp_events import *

# TCP Events
on_tcp_server_start = OnTCPServerStart()
on_tcp_server_connect = OnTCPServerConnect()
on_tcp_packet_received = OnTCPPacketReceived()
on_tcp_server_disconnect = OnTCPDisconnect()
on_tcp_server_stop = OnTCPServerStop()
on_tcp_server_error = OnTCPServerError()

# UDD Events
on_udp_server_start = OnUDPServerStart()
on_udp_packet_received = OnUDPPacketReceived()
on_udp_server_stop = OnUDPServerStop()


# TCP Client
on_client_created = OnClientCreated()
on_client_connected = OnClientConnect()
on_client_tcp_packet_received = OnClientTCPPacketReceived()
on_client_udp_packet_received = OnClientUDPPacketReceived()
on_client_disconnect = OnClientDisconnect()
on_client_error = OnClientError()

# GameServer
on_gameserver_start = OnGameServerStart()
on_gameserver_stop = OnGameServerStop()

# Remote Client
on_remote_client_created = OnRemoteClientCreated()
on_remote_client_connected = OnRemoteClientConnect()
on_remote_client_tcp_packet_received = OnRemoteClientTCPPacketReceived()
on_remote_client_udp_packet_received = OnRemoteClientUDPPacketReceived()
on_remote_client_disconnect = OnRemoteClientDisconnect()
on_remote_client_error = OnRemoteClientError()
