from .base_exception import JAMPBaseException


class UDPPacketSizeException(JAMPBaseException):
    """if the size of the udp_packet is invalid"""
