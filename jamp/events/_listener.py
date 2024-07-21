import threading


class Listener:
    def __init__(self, func: callable, threaded: bool = False, daemon_thread: bool = False) -> None:
        self.func: callable = func
        self.threaded: bool = threaded
        self.daemon_thread: bool = daemon_thread

    def call(self, *args, **kwargs):
        if self.threaded:
            threading.Thread(target=self.func, args=(args, kwargs), daemon=self.daemon_thread).start()
        else:
            self.func(*args, **kwargs)
