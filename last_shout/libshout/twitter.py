""" Function to send tweet to Twitter """
import sys

import twitter


def send_tweet(settings, tweet, encoding):
    """ Simple function to send tweet to Twitter """
    api = twitter.Api(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token_key=settings.access_key,
        access_token_secret=settings.access_secret,
        input_encoding=encoding,
    )

    try:
        status = api.PostUpdate(tweet)
    except UnicodeDecodeError:
        print("Last.fm statistics could not be encoded for Twitter.")
        sys.exit(2)
    except twitter.TwitterError as error:
        print(f"Twitter error: {error.message}")
        sys.exit(2)

    return status
