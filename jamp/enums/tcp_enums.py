from enum import Enum, auto


class TCPPayloadType(Enum):
    CONNECT = auto()
    DISCONNECT = auto()
