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
        self._config_file_updated = None

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
            self._config_file_updated = os.stat(filepath).st_mtime

        self._config["handlers"] = [import_from_string(handler)
                                    for handler in self._config["handlers"]]
        self._config["backends"] = [import_from_string(backend)
                                    for backend in self._config["backends"]]

    def get_handler_config(self, section):
        """
        Returns config for handler
        """
        return HandlerConfig(self, section)

    def get_backend_config(self, section):
        """
        Returns config for backend
        """
        return BackendConfig(self, section)

    def __getitem__(self, key):
        """
        Allows getting config data from config
        """
        if self._config_file and \
           self._config_file_updated < os.stat(self._config_file).st_mtime:
            logger.info("Config file changed! Reloading config file %s",
                        self._config_file)
            self.load(self._config_file)
        return self._config[key]


class ConfigWrapper(object):
    """
    Wrapper for specific config data
    """
    def __init__(self, config, section):
        """
        Gets a Config object and the name of the section of the config file
        from which retrieve information
        """
        self._config = config
        self._section = section
        self._fallbacks = {}

    def __getitem__(self, key):
        """
        Returns the value for the requested key in the config section
        """

        try:
            return self._config[self._section][key]
        except (KeyError, TypeError):
            pass
        try:
            return self._fallbacks[key]
        except KeyError:
            pass
        return None


class HandlerConfig(ConfigWrapper):
    """
    Config class for handlers
    """
    def __init__(self, config, section):
        super(HandlerConfig, self).__init__(config, section)
        self._fallbacks = {
            "interval": self._config["default_interval"]
        }


class BackendConfig(ConfigWrapper):
    """
    Config class for backends
    """
    pass
