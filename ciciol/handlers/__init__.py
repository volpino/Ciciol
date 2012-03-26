"""
Handlers for Ciciol

Handlers are called to get notifications from some source of information
(like Twitter, rss feeds, ...)
"""

import threading
from time import sleep


class HandlerRunner(threading.Thread):
    """
    Runner for threaded handlers
    """
    def __init__(self, Handler, config):
        """
        Receives an Handler and a config object
        """
        super(HandlerRunner, self).__init__()
        self.running = True
        self.config = config

        if hasattr(Handler, "handler_config"):
            h_config = config.get_handler_config(Handler.handler_config)
            self.handler = Handler(h_config)
        else:
            self.handler = Handler()

        self.backends = []
        for Backend in self.config["backends"]:
            if hasattr(Backend, "backend_config"):
                b_config = config.get_backend_config(Backend.backend_config)
                self.backends.append(Backend(b_config))
            else:
                self.backends.append(Backend())

    def stop(self):
        """
        Stops the thread execution
        """
        self.running = False

    def run(self):
        """
        Thread run method
        Checks for new notifications and sends it to all backends
        """
        while self.running:
            notifications = self.handler.get_notifications()
            if notifications:
                for backend in self.backends:
                    backend.notify(notifications)
            try:
                interval = self.handler.config["interval"]
            except (AttributeError, KeyError):
                interval = self.config["default_interval"]
            for _ in range(interval):
                if not self.running:
                    break
                sleep(1)
