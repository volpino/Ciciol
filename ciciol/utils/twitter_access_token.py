import webbrowser
import tweepy

from ciciol.handlers.twitter import CONSUMER_KEY, CONSUMER_SECRET

"""
Query the user for their consumer key/secret
then attempt to fetch a valid access token.
"""

if __name__ == "__main__":
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
