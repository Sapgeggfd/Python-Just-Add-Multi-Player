import pickle
from dataclasses import dataclass

from ..enums.udp_enum import UDPPayloadType
from ..exceptions.udp_exception import UDPPacketSizeException
from ..utils.static_settings import *


@dataclass
class UDPPacket:
    type: UDPPayloadType
    data: dict

    def dump(self):
        payload = pickle.dumps(self)
        if len(payload) <= UDP_PACKET_SIZE:
            return payload
        raise UDPPacketSizeException

    @staticmethod
    def load(payload) -> "UDPPacket":
        return pickle.loads(payload)
