import logging

import jamp
from jamp.utils.custom_logger import GameServerLogger

logging.basicConfig(level=logging.DEBUG)
l = GameServerLogger
# l = logging.getLogger()
l.debug("test Debug")
l.info("test info")
l.warning("test waring")
l.critical("test critical")


gs = jamp.GameServer()


gs.start()
