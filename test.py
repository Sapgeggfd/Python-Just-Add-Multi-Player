class Event:
    def __init__(self) -> None:
        self.__listener: list["function"] = []

    def on_trigger(self, func=None, **kwarg):
        print(func, kwarg)
        if func is None or type(func) != callable:
            # return None
            return lambda f: self.on_trigger(f)
        print(func, kwarg)
        self.__listener.append(func)

    def addListener(self, func):
        if func not in self.__listener:
            return
        self.__listener.append(func)

    def trigger(self, *args, **kwargs):
        for func in self.__listener:
            func(*args, **kwargs)


e = Event()


@e.on_trigger(kw="kw")
def test(*args, **kwargs):
    print(args)
    print(kwargs)


e.trigger()
