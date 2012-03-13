import webbrowser
import tweepy

from ciciol.handlers.twitter import CONSUMER_KEY, CONSUMER_SECRET


def twitter_access_token():
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

    # Give user the access token
    print 'Access token:'
    print ' Key: %s' % token.key
    print ' Secret: %s' % token.secret
