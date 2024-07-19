import logging
from logging import Logger, getLogger

TCPServerLogger: Logger = getLogger("TCPServerLogger")
TCPServerLogger.setLevel(logging.DEBUG)

GameServerLogger: Logger = getLogger("GameServerLogger")
GameServerLogger.setLevel(logging.DEBUG)

ClientLogger: Logger = getLogger("ClientLogger")
ClientLogger.setLevel(logging.DEBUG)
