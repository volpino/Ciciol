import logging
from ciciol.config import Config
from ciciol.handlers import HandlerRunner
from time import sleep

logger = logging.getLogger(__name__)


class Ciciol(object):
    """
    Main class for Ciciol
    """
    def __init__(self, config_fn=None):
        """
        Loads a config from config_fn or using autodiscover
        """
        self.config = Config()
        if config_fn:
            self.config.load(config_fn)
        else:
            self.config.autodiscover()

    def run(self):
        """
        Launches handlers in separate threads
        """
        threads = []

        for Handler in self.config["handlers"]:
            logger.info("Threading handler %s", Handler)
            runner = HandlerRunner(Handler, self.config)
            runner.start()
            threads.append(runner)

        try:
            while True:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            logger.info("Exiting and stopping all threads...")
            for thread in threads:
                thread.stop()
