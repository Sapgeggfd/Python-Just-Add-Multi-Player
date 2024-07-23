from ._base_event import Event


class OnGameServerStart(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """triggers if the GameServer is started"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)


class OnGameServerStop(Event):
    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        """triggers if the GameServer is stopt"""
        return super().register(func, threaded=threaded, daemon_thread=daemon_thread)
