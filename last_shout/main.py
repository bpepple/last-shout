""" Main project file """

import sys

from mastodon import Mastodon, MastodonIllegalArgumentError

from .libshout.lastfm import get_top_artist
from .libshout.options import create_parser
from .libshout.settings import LastShoutSettings
from .libshout.utils import create_music_stats

MASTODON_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"


def has_lastfm_credentials(settings: LastShoutSettings) -> bool:
    return bool(settings.last_user or not settings.last_access_key)


def has_mastodon_app_credentials(settings: LastShoutSettings) -> bool:
    return bool(
        (
            settings.mastodon_client_id
            and settings.mastodon_client_secret
            and settings.mastodon_api_base_url
        )
    )


def has_mastodon_user_credentials(settings) -> bool:
    return bool(settings.mastodon_user_token)


def create_mastodon_app(settings: LastShoutSettings) -> bool:
    app_name = "Last-Shout"
    app_url = "https://github.com/bpepple/last-shout"
    instance = input("Enter Mastodon instance (ex. 'https://mastodon.social'): ")

    client_id, client_secret = Mastodon.create_app(
        app_name,
        website=app_url,
        api_base_url=instance,
        redirect_uris=MASTODON_REDIRECT_URI,
    )

    if not (client_id or client_secret):
        return False

    settings.mastodon_client_id = client_id
    settings.mastodon_client_secret = client_secret
    settings.mastodon_api_base_url = instance
    settings.save()

    return True


def create_mastodon_user_token(settings: LastShoutSettings) -> bool:
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
            redirect_uris=MASTODON_REDIRECT_URI,
        )
    )

    auth = input("\nCopy the authorized code here to generate user token: ")
    try:
        user_token = mastodon.log_in(
            code=auth,
            scopes=["write"],
            redirect_uri=MASTODON_REDIRECT_URI,
        )
    except MastodonIllegalArgumentError:
        return False

    settings.mastodon_user_token = user_token
    settings.save()

    return True


def send_toot(settings: LastShoutSettings, toot_text: str):
    mastodon = Mastodon(
        access_token=settings.mastodon_user_token,
        api_base_url=settings.mastodon_api_base_url,
    )
    return mastodon.toot(toot_text)


def post_toot(settings, music_stats_txt):
    if not has_mastodon_app_credentials(settings) or not has_mastodon_user_credentials(
        settings
    ):
        print("Missing Mastodon credentials. Exiting...")
        sys.exit(2)

    status = send_toot(settings, music_stats_txt)
    print(f"Last.fm statistics posted to Mastodon at {status.created_at}")


def save_lastfm_credentials(settings):
    if has_lastfm_credentials(settings):
        settings.save()
    else:
        print("Missing Last.fm credentials. Unable to save.")
        sys.exit(0)


def main():
    """Main Function"""
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
            print("Unable to create Mastodon user token.")
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
        save_lastfm_credentials(settings)

    # If Last.fm are missing exit
    if not has_lastfm_credentials(settings):
        print("Missing Last.fm. Exiting...")
        sys.exit(2)

    artists = get_top_artist(
        settings.last_access_key, settings.last_user, opts.number, opts.period
    )
    music_stats_txt = create_music_stats(artists, opts.period)
    if not music_stats_txt:
        print("No results returned from Last.fm")
        exit(0)

    if opts.toot:
        post_toot(settings, music_stats_txt)

    if not opts.tweet and not opts.toot:
        print(music_stats_txt)


if __name__ == "__main__":
    sys.exit(main())
