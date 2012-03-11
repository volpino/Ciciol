import logging
from ciciol.config import Config
from ciciol.handlers import HandlerRunner
from time import sleep
import sys

logging.basicConfig(stream=sys.stderr,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)


class Ciciol(object):
    def __init__(self):
        self.config = Config()
        self.config.autodiscover()

    def run(self):
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
