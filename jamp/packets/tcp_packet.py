import pickle
from dataclasses import dataclass

from ..enums.tcp_server_enums import PayloadType
from ..utils.static_settings import TCP_HEADER_SIZE


@dataclass
class TCPPacket:
    type: PayloadType
    data: dict

    def dump(self):
        payload = pickle.dumps(self)

        print(f"{len(payload):<{TCP_HEADER_SIZE}}\nPayload{payload}")
        print()

        return f"{len(payload):<{TCP_HEADER_SIZE}}".encode() + payload

    @staticmethod
    def load(payload) -> "TCPPacket":
        return pickle.loads(payload)
