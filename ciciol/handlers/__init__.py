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
        self.running = True
        if hasattr(Handler, "handler_config"):
            h_config = config.get_handler_config(Handler.handler_config)
            self.handler = Handler(h_config)
        else:
            self.handler = Handler()
        self.config = config
        super(HandlerRunner, self).__init__()

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
                for Backend in self.config["backends"]:
                    backend = Backend()
                    backend.notify(notifications)

            for _ in range(self.handler.config["interval"]):
                if not self.running:
                    break
                sleep(1)
