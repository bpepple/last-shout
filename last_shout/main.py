""" Main project file """

import sys

from mastodon import Mastodon, MastodonIllegalArgumentError

from .libshout.lastfm import get_top_artist
from .libshout.options import create_parser
from .libshout.settings import LastShoutSettings
from .libshout.twitter import send_tweet
from .libshout.utils import build_twitter_string


def has_lastfm_credentials(settings):
    if not settings.last_user and settings.last_access_key:
        return False

    return True


def has_twitter_credentials(settings):
    if not (
        settings.consumer_key
        and settings.consumer_key
        and settings.access_key
        and settings.access_secret
    ):
        return False

    return True


def has_mastodon_app_credentials(settings):
    if not (
        settings.mastodon_client_id
        and settings.mastodon_client_secret
        and settings.mastodon_api_base_url
    ):
        return False

    return True


def has_mastodon_user_credentials(settings):
    if not settings.mastodon_user_token:
        return False
    return True


def create_mastodon_app(settings):
    instance = input("Enter Mastodon instance (ex. 'https://mastodon.social'): ")
    app_name = input("Enter name of application (ex. LastShout): ")
    app_url = input("End url of application: ")

    client_id, client_secret = Mastodon.create_app(
        app_name,
        website=app_url,
        api_base_url=instance,
        redirect_uris="urn:ietf:wg:oauth:2.0:oob",
        to_file="pytooter_clientcred.txt",
    )

    if not (client_id or client_secret):
        return False

    settings.mastodon_client_id = client_id
    settings.mastodon_client_secret = client_secret
    settings.mastodon_api_base_url = instance
    settings.save()

    return True


def create_mastodon_user_token(settings):
    mastodon = Mastodon(
        client_id=settings.mastodon_client_id,
        client_secret=settings.mastodon_client_secret,
        api_base_url=settings.mastodon_api_base_url,
    )
    # Uri to provide to client to grant authorization
    print("Go to the follow url to grant authorization from Mastodon.\n")
    print(
        mastodon.auth_request_url(
            client_id=settings.mastodon_client_id,
            redirect_uris="urn:ietf:wg:oauth:2.0:oob",
        )
    )

    auth = input("\nCopy the authorized code here to generate user token: ")
    try:
        user_token = mastodon.log_in(
            code=auth,
            scopes=["write"],
            redirect_uri="urn:ietf:wg:oauth:2.0:oob",
            to_file="pytooter_usercred.secret",
        )
    except MastodonIllegalArgumentError:
        return False

    settings.mastodon_user_token = user_token
    settings.save()

    return True


def sent_toot(settings, toot_text):
    mastodon = Mastodon(
        access_token=settings.mastodon_user_token,
        api_base_url=settings.mastodon_api_base_url,
    )
    status = mastodon.toot(toot_text)

    return status


def main():
    """ Main Function """
    settings = LastShoutSettings()
    parser = create_parser()
    opts = parser.parse_args()

    # Create Mastodon application
    if opts.create_mastodon_app:
        result = create_mastodon_app(settings)
        if result:
            print("Saved Mastodon application credentials to configuration file.")
        else:
            print("Unable to create application credentials.")
        sys.exit(0)

    # Create Mastodon user token
    if opts.create_mastodon_user:
        if not has_mastodon_app_credentials(settings):
            print("Missing Mastodon application credentials. Exiting...")
            sys.exit(2)
        result = create_mastodon_user_token(settings)
        if result:
            print("Saved Mastodon user token to configuration file.")
        else:
            print("Unable to create Mastododon user token.")
        sys.exit(0)

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
        if has_lastfm_credentials(settings):
            settings.save()
        else:
            print("Missing Last.fm credetials. Unable to save.")
            sys.exit(0)

    # Save Twitter options
    if opts.set_twitter:
        if has_twitter_credentials(settings):
            settings.save()
        else:
            print("Missing Twitter credentials. Unable to save.")
            sys.exit(0)

    # If Last.fm or Twitter credentials are missing exit
    if not has_lastfm_credentials(settings) or not has_twitter_credentials(settings):
        print("Missing Last.fm or Twitter credentials. Exitting...")
        sys.exit(2)

    artists = get_top_artist(
        settings.last_access_key, settings.last_user, opts.number, opts.period
    )
    twitter_text = build_twitter_string(artists, opts.period)

    if opts.tweet:
        status = send_tweet(settings, twitter_text, None)
        print(f"Last.fm statistics posted to Twitter at {status.created_at}")
    else:
        print(twitter_text)

    if opts.toot:
        if not has_mastodon_app_credentials(
            settings
        ) or not has_mastodon_user_credentials(settings):
            print("Missing Mastodon credentials. Exiting...")
            sys.exit(2)

        status = sent_toot(settings, twitter_text)
        print(f"Last.fm statistics posted to Mastodon at {status.created_at}")


if __name__ == "__main__":
    sys.exit(main())
