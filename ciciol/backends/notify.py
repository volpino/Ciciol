import pynotify
import tempfile
from time import sleep
import urllib
import logging
import os

logger = logging.getLogger(__name__)


class NotifyBackend(object):
    def notify(self, notifications):
        for notification in notifications:
            sender = message = photo = None
            try:
                sender, message, photo = notification
            except ValueError:
                pass
            if photo is not None:
                tempdir = tempfile.mkdtemp()
                tmp = os.path.join(tempdir, photo.split("/")[-1])

                logging.info("Getting image url %s to %s", photo, tmp)
                photo_content = urllib.urlopen(photo)
                with open(tmp, "w") as f:
                    f.write(photo_content.read())
                logging.info("Saved... %s", tmp)
                self._notify_one(sender, message, tmp)
                sleep(10)
            else:
                self._notify_one(sender, message)
                sleep(10)

    def _notify_one(self, sender, message, photo="dialog-information"):
        pynotify.init(sender)
        notification = pynotify.Notification(
            sender,
            message,
            photo
        )
        notification.show()
