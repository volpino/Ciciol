"""
libnotify backend module for Ciciol
"""

import pynotify
import tempfile
import urllib
import logging
import os
import shutil

logger = logging.getLogger(__name__)


class NotifyBackend(object):
    """
    libnotify backend for Ciciol
    """
    def __init__(self):
        self.tempdir = tempfile.mkdtemp()

    def __del__(self):
        shutil.rmtree(self.tempdir)

    def notify(self, notifications):
        """
        notify method
        """
        for notification in notifications:
            sender = message = photo = None
            try:
                sender, message, photo = notification
            except ValueError:
                sender, message = notification
            if photo is not None:
                tmp = os.path.join(self.tempdir, photo.split("/")[-1])
                if not os.path.exists(tmp):
                    logging.info("Saving image url %s to %s", photo, tmp)
                    photo_content = urllib.urlopen(photo)
                    with open(tmp, "w") as f:
                        f.write(photo_content.read())
                self._notify_one(sender, message, tmp)
            else:
                self._notify_one(sender, message)

    def _notify_one(self, sender, message, photo="dialog-information"):
        """
        Sends one notification with libnotify
        """
        pynotify.init(sender)
        notification = pynotify.Notification(
            sender,
            message,
            photo
        )
        notification.show()
