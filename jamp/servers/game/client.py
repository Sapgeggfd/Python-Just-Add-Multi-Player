import socket
from logging import Logger
from queue import PriorityQueue
from uuid import uuid4

import requests

from ...enums.tcp_enums import TCPPayloadType
from ...events.udp_tcp_client_events import *
from ...packets.tcp_packet import TCPPacket
from ...utils.custom_logger import ClientLogger
from ...utils.static_settings import *
from .exception import *


class Client:
    tcp_sock: socket.socket

    connected:bool
    disconnected:bool
    user_uuid: uuid4
    auth_token:str
    
    remote_ip:str
    
    def __init__(self, address, tcp_sock: socket.socket) -> None:
        self.logger: Logger = ClientLogger
        self.connected = False 
        self.disconnected = False

        self.address = address
        self.tcp_sock = tcp_sock 
        self._user_uuid = None
        
        self.udp_queue = PriorityQueue()
        
        self.remote_ip=self.tcp_sock.getpeername()
        

    @property
    def user_uuid(self)->uuid4:
        return self._user_uuid

    @user_uuid.setter
    def user_uuid(self, user_uuid: uuid4):
        if type(user_uuid) != uuid4:
            raise InvalidUserUUID(user_uuid=user_uuid,logger=self.logger)
        self._user_uuid = user_uuid
        self.connected = True
        
        
    def _wait_for_connect(self) -> bool:
        with self.tcp_sock as client_sock:
            while self.connected:
                try:
                    payload_size: str = client_sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8")
                    if payload_size.isdecimal():
                        payload = client_sock.recv(int(payload_size))
                        packet = TCPPacket.load(payload)
                        self.user_uuid(packet.data.get("user_uuid"))
                        if packet.type == TCPPayloadType.CONNECT and self._auth_player():
                            self.connected = True
                            on_client_connect.trigger(client=self)
                except (EOFError, ConnectionResetError) as e:
                    self.error_disconnect(exception=e,connection_error=True)
            
            return True
        
    def _auth_player(self)->bool:
        if not PLAYER_AUTH:
            return True
        else:
            try:
                if self.auth_token != None:
                    self._call_auth_server()                        
                else:
                    self.logger.warn("User with empty Auth-Token tried to join the Server")
            except (AuthError,AuthServerError) as e:
                self.error_disconnect(exception=e)
                
    def _call_auth_server(self):
        try:
            payload = {"user_uuid":self.user_uuid,"auth_token":self.auth_token}
            if r := requests.post(f"{PLAYER_AUTH_SERVER_URL}/auth/player/",json=payload,cert=CERTIFICATE if CERTIFICATE else None):
                if r.status_code != 200:
                    raise AuthError(auth_token=self.auth_token,logger=self.logger)
        except requests.RequestException as e:
            raise AuthServerError(e)
        
    def _handle_tcp_packets(self):
        with self.tcp_sock as client_sock:
            while self.connected:
                try:
                    payload_size: str = client_sock.recv(TCP_HEADER_SIZE)[:TCP_HEADER_SIZE].decode("utf-8")
                    if payload_size.isdecimal():
                        payload = client_sock.recv(int(payload_size))
                        packet = TCPPacket.load(payload)
                        on_tcp_packet_received.trigger(client = self,packet=packet)
                except (EOFError, ConnectionResetError):
                    break
                
    def handle_udp_packet(self,packet):
        self.udp_queue((packet,))
            
        
    
    @on_tcp_packet_received.register(packet_type=TCPPayloadType.DISCONNECT)
    def handle_disconcert_package(self,package:TCPPacket)->None:
        self.disconnect(reason="user-disconcert",msg="Thx for Playing :D")
    
    def send(self,packet:TCPPacket)->None:
        try:
            self.logger.debug(f"Sending Packet to user [{self.user_uuid.hex}] type:{packet.type} payload:{packet.data}")
            payload = packet.dump()
            self.tcp_sock.sendall(payload)
        except BrokenPipeError as e:
            self.error_disconnect(send_exception = e,connection_error=True)
            

    def disconnect(self,reason=None,msg=None,**kwargs):
        """Disconnects a user from the server

        Args:
            reason (_type_, optional): _description_. Defaults to None.
        """
        
        packet = TCPPacket(type=TCPPayloadType.DISCONNECT,data={"reason":reason,"msg":msg,**kwargs})
        self.send(packet)
        self.tcp_sock.close()
        self.connected = False
        self.disconnected = True
        on_client_disconnect.trigger(client=self)
        self.logger.info(f"User [{self.user_uuid.hex}] disconnected {kwargs if kwargs else ""}")

    def error_disconnect(self,exception:Exception,connection_error:False):
        if not connection_error:
            packet = TCPPacket(type=TCPPayloadType.DISCONNECT,data={"reason":type(exception),"args":exception.args})
            self.send(packet=packet)
        self.tcp_sock.close()
        self.connected = False
        self.disconnected = True
        on_client_disconnect.trigger(client=self)
        self.logger.warning(f"User Disconnect with {"Connection ERROR" if connection_error else "ERROR"}",exc_info=exception)
