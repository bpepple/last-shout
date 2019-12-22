""" Main project file """

import os
import sys

# Append sys.path so imports work.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from last_shout.libshout.lastfm import get_top_artist
from last_shout.libshout.options import create_parser
from last_shout.libshout.settings import LastShoutSettings
from last_shout.libshout.twitter import send_tweet
from last_shout.libshout.utils import build_twitter_string


SETTINGS = LastShoutSettings()


def main():
    """ Main Function """
    parser = create_parser()
    opts = parser.parse_args()

    # Get Last.fm credentials
    if opts.user:
        SETTINGS.last_user = opts.user

    if opts.last_access_key:
        SETTINGS.last_access_key = opts.last_access_key

    # Get Twitter credentials
    if opts.consumer_key:
        SETTINGS.consumer_key = opts.consumer_key

    if opts.consumer_secret:
        SETTINGS.consumer_secret = opts.consumer_secret

    if opts.access_key:
        SETTINGS.access_key = opts.access_key

    if opts.access_secret:
        SETTINGS.access_secret = opts.access_secret

    # Save Last.fm options
    if opts.set_lastfm:
        if SETTINGS.last_user and SETTINGS.last_access_key:
            SETTINGS.save()
        else:
            print("Missing Last.fm credetials. Unable to save.")
            sys.exit(0)

    # Save Twitter options
    if opts.set_twitter:
        if (
            SETTINGS.consumer_key
            and SETTINGS.consumer_secret
            and SETTINGS.access_key
            and SETTINGS.access_secret
        ):
            SETTINGS.save()
        else:
            print("Missing Twitter credentials. Unable to save.")
            sys.exit(0)

    # If Last.fm or Twitter credentials are missing exit
    if (
        not SETTINGS.last_user
        or not SETTINGS.last_access_key
        or not SETTINGS.consumer_key
        or not SETTINGS.consumer_secret
        or not SETTINGS.access_key
        or not SETTINGS.access_secret
    ):
        print("Missing Last.fm or Twitter credentials. Exitting...")
        sys.exit(2)

    artists = get_top_artist(
        SETTINGS.last_access_key, SETTINGS.last_user, opts.number, opts.period
    )
    twitter_text = build_twitter_string(artists, opts.period)
    send_tweet(SETTINGS, twitter_text, None)


if __name__ == "__main__":
    sys.exit(main())
