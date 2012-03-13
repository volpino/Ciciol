import webbrowser
import tweepy
from ciciol.handlers.twitter import CONSUMER_KEY, CONSUMER_SECRET


def twitter():
    """
    Attempt to fetch a valid access token.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Open authorization URL in browser
    webbrowser.open(auth.get_authorization_url())

    # Ask user for verifier pin
    pin = raw_input('Verification pin number from twitter.com: ').strip()

    # Get access token
    token = auth.get_access_token(verifier=pin)

    print
    print "Add this to your configuration file in the twitter section:"
    print
    print "access_key: %s" % token.key
    print "access_secret %s" % token.secret
