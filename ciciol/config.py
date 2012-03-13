"""
Module for managing Ciciol's config files
"""

import logging
import yaml
import os
from collections import defaultdict
from ciciol.helpers import import_from_string

CONFIG_DEFAULT = {
    "handlers": {
        "ciciol.handlers.twitter.TwitterHandler",
    },
    "backends": {
        "ciciol.backends.notify.NotifyBackend",
    },
    "default_interval": 180,
}

CONFIG_FILENAMES = ["ciciol", "ciciolrc", "ciciol.yml"]
CONFIG_AUTODISCOVER_PATHS = [".", os.environ['HOME']]

logger = logging.getLogger(__name__)


class Config(object):
    """
    Class that handles configuration
    """
    def __init__(self):
        """
        __init__ for Config
        """
        self._config = defaultdict(lambda: None)
        self._config.update(CONFIG_DEFAULT)
        self._config_file = None

    def autodiscover(self):
        """
        Tries to autodiscover a config file, then it loads it.
        If no config file is found the default config is loaded.
        """
        filenames = CONFIG_FILENAMES + ["." + fn for fn in CONFIG_FILENAMES]
        for path in CONFIG_AUTODISCOVER_PATHS:
            for filename in filenames:
                filepath = os.path.join(path, filename)
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    self.load(filepath)
                    return
        logging.warn("No config file found! Using default data")
        self.load()

    def load(self, filepath=None):
        """
        Loads a config file from filepath
        """
        if filepath:
            logger.info("Loading config file %s", filepath)
            with open(filepath) as f:
                self._config_file = filepath
                self._config.update(yaml.load(f))

        self._config["handlers"] = [import_from_string(handler)
                                    for handler in self._config["handlers"]]
        self._config["backends"] = [import_from_string(backend)
                                    for backend in self._config["backends"]]

    def get_handler_config(self, handler):
        """
        Returns config for handler
        """
        h_config = defaultdict(lambda: None)
        if self[handler]:
            h_config.update(self[handler])
        if not "interval" in h_config:
            h_config["interval"] = self["default_interval"]
        return h_config

    def __getitem__(self, key):
        """
        Allows getting config data from config
        """
        return self._config[key]
