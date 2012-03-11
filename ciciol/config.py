"""
Module for managing Ciciol's config files
"""

import logging
import yaml
import os

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
    def __init__(self, config_file=None):
        self._config = CONFIG_DEFAULT.copy()
        self._config_file = config_file

    def autodiscover(self):
        filenames = CONFIG_FILENAMES + ["." + fn for fn in CONFIG_FILENAMES]
        for path in CONFIG_AUTODISCOVER_PATHS:
            for filename in filenames:
                filepath = os.path.join(path, filename)
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    logger.info("Loading config file %s", filepath)
                    self.load(filepath)
                    return
        logging.warn("No config file found! Using default data")
        self.load()

    def _import_class(self, path):
        splitted = path.split(".")
        cls = splitted[-1]
        module = __import__(".".join(splitted[:-1]), fromlist=[cls])
        return getattr(module, splitted[-1])

    def load(self, filename=None):
        if filename:
            with open(filename) as f:
                self._config.update(yaml.load(f))

        self._config["handlers"] = [self._import_class(handler)
                                   for handler in self._config["handlers"]]
        self._config["backends"] = [self._import_class(backend)
                                    for backend in self._config["backends"]]

    def get_handler_config(self, handler):
        h_config = self[handler]
        if not "interval" in h_config:
            h_config["interval"] = self["default_interval"]
        return h_config

    def __getitem__(self, key):
        return self._config[key]
