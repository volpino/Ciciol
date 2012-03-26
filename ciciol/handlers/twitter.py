"""
Twitter handler module for Ciciol
"""

import tweepy
import re
import logging

logger = logging.getLogger(__name__)

# ok, this is plaintext. Any way of encrypt this would be completely useless.
# i don't know why somebody would steal this but anyway don't be a dick.
CONSUMER_KEY = "voOKgadzgujaLJ0DeMLHnw"
CONSUMER_SECRET = "xv8ofN6jeHkpZ0RcLLXVQUBQtQ0JDMzaYKXDrz7HYM"


class TwitterHandler():
    """
    Handler for Twitter
    """
    handler_config = "twitter"

    def __init__(self, config):
        self.config = config

        self.auth = tweepy.OAuthHandler(CONSUMER_KEY,
                                        CONSUMER_SECRET)

        if self.config["access_key"] and self.config["access_secret"]:
            self.authenticated = True
            self.auth.set_access_token(self.config["access_key"],
                                       self.config["access_secret"])
        else:
            self.authenticated = False

        self.api = tweepy.API(self.auth)
        self.sent_notifications = []

    def _check_filter(self, value, filter_, exclude=False):
        """
        filter_ is an iterable of regex objects.
        Returns True if value matches at least one of the regexes or
        filter_ is empty
        """
        if not filter_:
            return True
        for regex in filter_:
            match = re.search(regex, value)

            if match is not None:
                return not exclude
        return exclude

    def get_notifications(self):
        """
        Returns a list of notifications
        """
        results = []

        try:
            if self.authenticated:
                timeline = self.api.home_timeline()
            else:
                timeline = self.api.public_timeline()[:5]
        except tweepy.TweepError, exc:
            logger.warn("Twitter API error: %r", exc)
            return []

        for tweet in timeline:
            if tweet.id in self.sent_notifications:
                continue

            text = tweet.text
            author = tweet.author.screen_name
            conf = self.config

            filter_include = (
                self._check_filter(author, conf["author_include"]) or
                self._check_filter(text, conf["text_include"])
            )

            filter_exclude = (
                self._check_filter(author, conf["author_exclude"], True) and
                self._check_filter(text, conf["text_exclude"], True)
            )

            if filter_include and filter_exclude:
                results.append(
                    (tweet.author.name, text, tweet.author.profile_image_url)
                )
                self.sent_notifications.append(tweet.id)

        searches = self.config["search"] or []
        for search in searches:
            for tweet in self.api.search(search):
                if tweet.id in self.sent_notifications:
                    continue
                results.append(
                    (tweet.from_user_name, tweet.text, tweet.profile_image_url)
                )
                self.sent_notifications.append(tweet.id)

        return results
