import pickle
from dataclasses import dataclass

from ..enums.udp_enum import UDPPayloadType
from ..utils.static_settings import *


@dataclass
class UDPPacket:
    type: UDPPayloadType
    data: dict

    def dump(self):
        payload = pickle.dumps(self)

        print(f"{len(payload):<{TCP_HEADER_SIZE}}\nPayload{payload}")
        print()

        return f"{len(payload):<{TCP_HEADER_SIZE}}".encode() + payload

    @staticmethod
    def load(payload) -> "UDPPacket":
        return pickle.loads(payload)
