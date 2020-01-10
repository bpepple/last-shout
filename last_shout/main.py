""" Main project file """

import sys

from .libshout.lastfm import get_top_artist
from .libshout.options import create_parser
from .libshout.settings import LastShoutSettings
from .libshout.twitter import send_tweet
from .libshout.utils import build_twitter_string


def main():
    """ Main Function """
    settings = LastShoutSettings()
    parser = create_parser()
    opts = parser.parse_args()

    # Get Last.fm credentials
    if opts.user:
        settings.last_user = opts.user

    if opts.last_access_key:
        settings.last_access_key = opts.last_access_key

    # Get Twitter credentials
    if opts.consumer_key:
        settings.consumer_key = opts.consumer_key

    if opts.consumer_secret:
        settings.consumer_secret = opts.consumer_secret

    if opts.access_key:
        settings.access_key = opts.access_key

    if opts.access_secret:
        settings.access_secret = opts.access_secret

    # Save Last.fm options
    if opts.set_lastfm:
        if settings.last_user and settings.last_access_key:
            settings.save()
        else:
            print("Missing Last.fm credetials. Unable to save.")
            sys.exit(0)

    # Save Twitter options
    if opts.set_twitter:
        if (
            settings.consumer_key
            and settings.consumer_secret
            and settings.access_key
            and settings.access_secret
        ):
            settings.save()
        else:
            print("Missing Twitter credentials. Unable to save.")
            sys.exit(0)

    # If Last.fm or Twitter credentials are missing exit
    if (
        not settings.last_user
        or not settings.last_access_key
        or not settings.consumer_key
        or not settings.consumer_secret
        or not settings.access_key
        or not settings.access_secret
    ):
        print("Missing Last.fm or Twitter credentials. Exitting...")
        sys.exit(2)

    artists = get_top_artist(
        settings.last_access_key, settings.last_user, opts.number, opts.period
    )
    twitter_text = build_twitter_string(artists, opts.period)
    send_tweet(settings, twitter_text, None)


if __name__ == "__main__":
    sys.exit(main())
