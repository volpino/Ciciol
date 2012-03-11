"""
Dummy backend module for Ciciol
"""

import logging

logger = logging.getLogger(__name__)


class DummyBackend(object):
    """
    Dummy backend for Ciciol
    """

    def notify(self, notifications):
        """
        Given a list of notifications notifies them to the user

        A notification is a tuple with sender, message and optionally a photo
        url
        """
        for notification in notifications:
            logger.info("New notification: %s", notification)
