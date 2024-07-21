from typing import Protocol


class GameServer(Protocol): ...


class UDPServer:
    host: str
    port: int
    game_server: GameServer

    def __init__(self, host: str, port: int, game_server: GameServer) -> None:
        self.host = host
        self.port = port
        self.game_server = game_server
