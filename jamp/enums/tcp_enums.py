from enum import Enum, auto


class TCPPayloadType(Enum):
    CONNECT = auto()
    BROADCAST = auto()
    DISCONNECT = auto()
