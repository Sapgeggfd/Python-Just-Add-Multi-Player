class JAMPBaseException(Exception):
    """The Base Exception for the JAMP Packages"""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
