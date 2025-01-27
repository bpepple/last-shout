""" Main project file """

import sys

from atproto import Client
from atproto_client.models.app.bsky.feed.post import CreateRecordResponse
from atproto_core.exceptions import AtProtocolError
from mastodon import Mastodon, MastodonIllegalArgumentError

from .libshout.lastfm import get_top_artist
from .libshout.options import create_parser
from .libshout.settings import LastShoutSettings
from .libshout.utils import create_music_stats

MASTODON_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"


def has_lastfm_credentials(settings: LastShoutSettings) -> bool:
    return bool(settings.last_user and settings.last_access_key)


def has_bluesky_credentials(settings: LastShoutSettings) -> bool:
    return bool(settings.bluesky_handle or not settings.bluesky_password)


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


def _send_toot(settings: LastShoutSettings, toot_text: str):
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

    status = _send_toot(settings, music_stats_txt)
    print(f"Last.fm statistics posted to Mastodon at {status.created_at}")


def _send_skeet(settings: LastShoutSettings, music_stats_txt) -> CreateRecordResponse:
    client = Client()
    client.login(settings.bluesky_handle, settings.bluesky_password)
    return client.send_post(text=music_stats_txt)


def post_skeet(settings, music_stats_txt):
    if not has_bluesky_credentials(settings):
        print("Missing Bluesky credentials. Exiting...")
        sys.exit(2)

    try:
        _send_skeet(settings, music_stats_txt)
    except AtProtocolError as e:
        print("Failed to send skeet. %s", e)
    print("Last.fm statistics posted to Bluesky")


def save_bluesky_credentials(settings: LastShoutSettings):
    if has_bluesky_credentials(settings):
        settings.save()
    else:
        print("Missing Bluesky credentials. Unable to save.")
        sys.exit(0)


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
        if create_mastodon_app(settings):
            print("Saved Mastodon application credentials to configuration file.")
        else:
            print("Unable to create application credentials.")
        sys.exit(0)

    # Create Mastodon user token
    if opts.create_mastodon_user:
        if not has_mastodon_app_credentials(settings):
            print("Missing Mastodon application credentials. Exiting...")
            sys.exit(2)
        if create_mastodon_user_token(settings):
            print("Saved Mastodon user token to configuration file.")
        else:
            print("Unable to create Mastodon user token.")
        sys.exit(0)

    # Get Last.fm credentials
    if opts.user:
        settings.last_user = opts.user

    if opts.last_access_key:
        settings.last_access_key = opts.last_access_key

    if opts.set_lastfm:
        save_lastfm_credentials(settings)

    if not has_lastfm_credentials(settings):
        print("Missing Last.fm. Exiting...")
        sys.exit(2)

    # Bluesky
    if opts.bluesky_handle:
        settings.bluesky_handle = opts.bluesky_handle

    if opts.bluesky_password:
        settings.bluesky_password = opts.bluesky_password

    if opts.set_bluesky:
        save_bluesky_credentials(settings)

    # Get last.fm stats
    artists = get_top_artist(
        settings.last_access_key, settings.last_user, opts.number, opts.period
    )
    music_stats_txt = create_music_stats(artists, opts.period)
    if not music_stats_txt:
        print("No results returned from Last.fm")
        exit(0)

    if opts.toot:
        post_toot(settings, music_stats_txt)

    if opts.skeet:
        post_skeet(settings, music_stats_txt)

    if not opts.tweet and not opts.toot:
        print(music_stats_txt)


if __name__ == "__main__":
    sys.exit(main())
