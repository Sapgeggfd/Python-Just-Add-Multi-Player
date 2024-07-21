class Event:
    def __init__(self, name: str) -> None:
        self.__listeners: list["function"] = []

    def register(self, func=None):
        if func == None:
            return lambda f: self.register(f)
        self._register_listener(func)

    def _register_listener(self, func):
        if func not in self.__listeners:
            self.__listeners.append(func)

    def unregister_listeners(self, listener: "function"):
        try:
            self.__listeners.remove(listener)
        except ValueError:
            pass

    def trigger(self, *args, **kwargs):
        for listeners in self.__listeners:
            listeners(*args, **kwargs)
