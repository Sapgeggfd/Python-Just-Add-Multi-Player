class Event:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.handlers: list["function"] = []

    def register_handler(self, handler: "function"):
        self.handlers.append(handler)

    def unregister_handler(self, handler: "function"):
        try:
            self.handlers.remove(handler)
        except ValueError:
            pass

    def trigger(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)
