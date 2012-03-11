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
    def __init__(self, config):
        self.config = config.get_handler_config("twitter")
        self.auth = tweepy.OAuthHandler(CONSUMER_KEY,
                                        CONSUMER_SECRET)
        self.auth.set_access_token(self.config["access_key"],
                                   self.config["access_secret"])
        self.api = tweepy.API(self.auth)
        self.config["author_include"] = [re.compile(regex) for regex in
                                         self.config["author_include"]]
        self.config["author_exclude"] = [re.compile(regex) for regex in
                                         self.config["author_exclude"]]
        self.config["text_include"] = [re.compile(regex) for regex in
                                       self.config["text_include"]]
        self.config["text_exclude"] = [re.compile(regex) for regex in
                                       self.config["text_exclude"]]
        self.sent_notifications = []

    def _check_filter(value, filter_):
        """
        filter_ is an iterable of regex objects.
        Returns True if value matches at least one of the regexes.
        """
        for regex in filter_:
            if regex.search(value) is not None:
                return True
        return False

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
            author = tweet.author.name
            conf = self.config

            no_filters = not any(conf["author_include"], conf["text_include"],
                                 conf["author_exclude"], conf["text_exclude"])

            include = (self._check_filter(author, conf["author_include"]) or \
                       self._check_filter(text, conf["text_include"]))

            exclude = (self._check_filter(author, conf["author_exclude"]) or \
                       self._check_filter(author, conf["text_exclude"]))

            if no_filters or (include and not exclude):
                results.append((author, text, tweet.author.profile_image_url))
                self.sent_notifications.append(tweet.id)

        return results
