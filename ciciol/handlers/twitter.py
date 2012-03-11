"""
Twitter handler module for Ciciol
"""

import tweepy
import re

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
        self.auth.set_access_token(self.config["access_key"],
                                   self.config["access_secret"])
        self.api = tweepy.API(self.auth)
        self.config["author_include"] = self._regex_compile(
            self.config["author_include"]
        )
        self.config["author_exclude"] = self._regex_compile(
            self.config["author_exclude"]
        )
        self.config["text_include"] = self._regex_compile(
            self.config["text_include"]
        )
        self.config["text_exclude"] = self._regex_compile(
            self.config["text_exclude"]
        )
        self.sent_notifications = []

    def _regex_compile(self, regex_list):
        """
        Converts a list of regexes strings to a list of compiled regexes
        """
        if regex_list:
            return [re.compile(regex) for regex in regex_list]
        else:
            return []

    def _check_filter(self, value, filter_, exclude=False):
        """
        filter_ is an iterable of regex objects.
        Returns True if value matches at least one of the regexes or
        filter_ is empty
        """
        if not filter_:
            return True
        for regex in filter_:
            if regex.search(value) is not None:
                return not exclude
        return exclude

    def get_notifications(self):
        """
        Returns a list of notifications
        """
        results = []

        timeline = self.api.home_timeline()
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

            if (filter_include and filter_exclude):
                results.append(
                    (tweet.author.name, text, tweet.author.profile_image_url)
                )
                self.sent_notifications.append(tweet.id)

        return results
