import pickle
from dataclasses import dataclass

from ..enums.tcp_enums import TCPPayloadType
from ..utils.static_settings import TCP_HEADER_SIZE


@dataclass
class TCPPacket:
    type: TCPPayloadType
    data: dict

    def dump(self):
        payload = pickle.dumps(self)

        # print(f"{len(payload):<{TCP_HEADER_SIZE}}".encode() + payload)

        return f"{len(payload):<{TCP_HEADER_SIZE}}".encode() + payload

    @staticmethod
    def load(payload) -> "TCPPacket":
        return pickle.loads(payload)
