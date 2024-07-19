import logging
from logging import Logger
from typing import Any
from uuid import uuid4

from ...exceptions.base_exception import JAMPBaseException
from ...packets.tcp_packet import TCPPacket


class AuthError(JAMPBaseException):
    """Exception for invalid Authorization"""

    def __init__(self, auth_token, logger: Logger = logging.getLogger(), *args: object) -> None:
        super().__init__(*args)

        logger.warning(msg=f"User with invalid Auth-Token [{auth_token}] tried to join the Server")


class AuthServerError(JAMPBaseException):
    """Exception for a failure of the Player-Auth-Server"""

    def __init__(self, request_exception=None, logger: Logger = logging.getLogger(), *args: object) -> None:
        super().__init__(*args)

        logger.critical(msg="AUTH-SERVER did not Respond", exc_info=request_exception)


class InvalidPackageType(JAMPBaseException):
    """Exception for invalid Package Types"""

    def __init__(
        self, user_uuid: uuid4 = None, logger: Logger = logging.getLogger(), package: TCPPacket = None, *args: object
    ) -> None:
        super().__init__(*args)

        logger.warning(msg=f"User [{user_uuid.hex}] send invalid Package Type: {package.type}")


class InvalidUserUUID(JAMPBaseException):
    def __init__(self, user_uuid: Any = None, logger: Logger = logging.getLogger(), *args: object) -> None:
        super().__init__(*args)

        logger.warning(msg=f"User has invalid UUID: {user_uuid}")
