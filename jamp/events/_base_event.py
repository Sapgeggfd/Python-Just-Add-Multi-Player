from ._listener import Listener


class Event:
    def __init__(self) -> None:
        self.__listeners: list[Listener] = []

    def register(self, func=None, *, threaded: bool = False, daemon_thread: bool = False):
        if func == None:
            return lambda f: self.register(f)
        new_listener = Listener(func=func, threaded=threaded, daemon_thread=daemon_thread)
        self._register_listener(new_listener)

    def trigger(self, *args, **kwargs) -> None: ...

    def _register_listener(self, listener: Listener):
        if listener not in self.__listeners:
            self.__listeners.append(listener)

    def _call_listeners(self, *args, **kwargs) -> None:
        for listener in self.__listeners:
            listener.call(*args, **kwargs)
