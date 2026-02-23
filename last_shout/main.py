"""Main project file with improved error handling and code quality."""

import logging
import sys

from atproto import Client
from atproto_core.exceptions import AtProtocolError
from mastodon import Mastodon, MastodonError, MastodonIllegalArgumentError

from .libshout.lastfm import get_top_artist
from .libshout.options import create_parser
from .libshout.settings import LastShoutSettings
from .libshout.utils import create_atproto_txt, create_mastodon_txt

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

MASTODON_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"


class LastShoutError(Exception):
    """Base exception for Last-Shout application."""

    pass


class CredentialsError(LastShoutError):
    """Raised when credentials are missing or invalid."""

    pass


class PostingError(LastShoutError):
    """Raised when posting to social media fails."""

    pass


def has_lastfm_credentials(settings: LastShoutSettings) -> bool:
    """Check if Last.fm credentials are available."""
    return bool(settings.last_user and settings.last_access_key)


def has_bluesky_credentials(settings: LastShoutSettings) -> bool:
    """Check if Bluesky credentials are available."""
    return bool(settings.bluesky_handle and settings.bluesky_password)


def has_mastodon_app_credentials(settings: LastShoutSettings) -> bool:
    """Check if Mastodon app credentials are available."""
    return bool(
        settings.mastodon_client_id
        and settings.mastodon_client_secret
        and settings.mastodon_api_base_url
    )


def has_mastodon_user_credentials(settings: LastShoutSettings) -> bool:
    """Check if Mastodon user credentials are available."""
    return bool(settings.mastodon_user_token)


def create_mastodon_app(settings: LastShoutSettings) -> bool:
    """Create a Mastodon application and save credentials."""
    app_name = "Last-Shout"
    app_url = "https://github.com/bpepple/last-shout"

    try:
        instance = input("Enter Mastodon instance (ex. 'https://mastodon.social'): ").strip()
        if not instance:
            logger.error("No instance provided")
            return False

        if not instance.startswith(("http://", "https://")):
            instance = f"https://{instance}"

        client_id, client_secret = Mastodon.create_app(
            app_name,
            website=app_url,
            api_base_url=instance,
            redirect_uris=MASTODON_REDIRECT_URI,
        )

        if not (client_id and client_secret):
            logger.error("Failed to create Mastodon app")
            return False

        settings.mastodon_client_id = client_id
        settings.mastodon_client_secret = client_secret
        settings.mastodon_api_base_url = instance
        settings.save()

        logger.info("Successfully created Mastodon app")
        return True

    except MastodonError as e:
        logger.error(f"Failed to create Mastodon app: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error creating Mastodon app: {e}")
        return False


def create_mastodon_user_token(settings: LastShoutSettings) -> bool:
    """Create a Mastodon user token and save it."""
    try:
        mastodon = Mastodon(
            client_id=settings.mastodon_client_id,
            client_secret=settings.mastodon_client_secret,
            api_base_url=settings.mastodon_api_base_url,
        )

        # Uri to provide to client to grant authorization
        auth_url = mastodon.auth_request_url(
            client_id=settings.mastodon_client_id,
            redirect_uris=MASTODON_REDIRECT_URI,
        )

        print("Go to the following URL to grant authorization from Mastodon:")
        print(f"{auth_url}\n")

        auth_code = input("Copy the authorized code here to generate user token: ").strip()
        if not auth_code:
            logger.error("No authorization code provided")
            return False

        user_token = mastodon.log_in(
            code=auth_code,
            scopes=["write"],
            redirect_uri=MASTODON_REDIRECT_URI,
        )

        settings.mastodon_user_token = user_token
        settings.save()

        logger.info("Successfully created Mastodon user token")
        return True

    except MastodonIllegalArgumentError as e:
        logger.error(f"Invalid authorization code: {e}")
        return False
    except MastodonError as e:
        logger.error(f"Mastodon error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error creating user token: {e}")
        return False


def _send_toot(settings: LastShoutSettings, toot_text: str):
    """Send a toot to Mastodon."""
    try:
        mastodon = Mastodon(
            access_token=settings.mastodon_user_token,
            api_base_url=settings.mastodon_api_base_url,
        )
        return mastodon.toot(toot_text)
    except MastodonError as e:
        raise PostingError(f"Failed to send toot: {e}") from e


def post_toot(settings: LastShoutSettings, music_stats_txt: str) -> None:
    """Post Last.fm statistics to Mastodon."""
    if not has_mastodon_app_credentials(settings) or not has_mastodon_user_credentials(settings):
        raise CredentialsError("Missing Mastodon credentials")

    try:
        status = _send_toot(settings, music_stats_txt)
        logger.info(f"Last.fm statistics posted to Mastodon at {status.created_at}")
    except PostingError:
        raise
    except Exception as e:
        raise PostingError(f"Unexpected error posting to Mastodon: {e}") from e


def post_skeet(settings: LastShoutSettings, music_stats_txt) -> None:
    """Post Last.fm statistics to Bluesky."""
    if not has_bluesky_credentials(settings):
        raise CredentialsError("Missing Bluesky credentials")

    try:
        client = Client()
        client.login(settings.bluesky_handle, settings.bluesky_password)
        client.send_post(text=music_stats_txt)
        logger.info("Last.fm statistics posted to Bluesky")
    except AtProtocolError as e:
        raise PostingError(f"Failed to send skeet: {e}") from e
    except Exception as e:
        raise PostingError(f"Unexpected error posting to Bluesky: {e}") from e


def save_bluesky_credentials(settings: LastShoutSettings) -> None:
    """Save Bluesky credentials to settings."""
    if not has_bluesky_credentials(settings):
        raise CredentialsError("Missing Bluesky credentials. Unable to save.")
    settings.save()
    logger.info("Bluesky credentials saved")


def save_lastfm_credentials(settings: LastShoutSettings) -> None:
    """Save Last.fm credentials to settings."""
    if not has_lastfm_credentials(settings):
        raise CredentialsError("Missing Last.fm credentials. Unable to save.")
    settings.save()
    logger.info("Last.fm credentials saved")


def get_music_stats(settings: LastShoutSettings, number: int, period: str):
    """Get Last.fm music statistics."""
    try:
        return get_top_artist(settings.last_access_key, settings.last_user, number, period)
    except Exception as e:
        raise LastShoutError(f"Failed to get Last.fm statistics: {e}") from e


def main() -> int:
    """Main function with improved error handling."""
    try:
        settings = LastShoutSettings()
        parser = create_parser()
        opts = parser.parse_args()

        # Handle Mastodon app creation
        if opts.create_mastodon_app:
            success = create_mastodon_app(settings)
            message = (
                "Saved Mastodon application credentials to configuration file."
                if success
                else "Unable to create application credentials."
            )
            print(message)
            return 0 if success else 1

        # Handle Mastodon user token creation
        if opts.create_mastodon_user:
            if not has_mastodon_app_credentials(settings):
                print("Missing Mastodon application credentials. Exiting...")
                return 2

            success = create_mastodon_user_token(settings)
            message = (
                "Saved Mastodon user token to configuration file."
                if success
                else "Unable to create Mastodon user token."
            )
            print(message)
            return 0 if success else 1

        # Handle Last.fm credentials
        if opts.user:
            settings.last_user = opts.user
        if opts.last_access_key:
            settings.last_access_key = opts.last_access_key
        if opts.set_lastfm:
            save_lastfm_credentials(settings)
            return 0

        if not has_lastfm_credentials(settings):
            print("Missing Last.fm credentials. Exiting...")
            return 2

        # Handle Bluesky credentials
        if opts.bluesky_handle:
            settings.bluesky_handle = opts.bluesky_handle
        if opts.bluesky_password:
            settings.bluesky_password = opts.bluesky_password
        if opts.set_bluesky:
            save_bluesky_credentials(settings)
            return 0

        # Get Last.fm statistics
        artists = get_music_stats(settings, opts.number, opts.period)

        # Post to social media or print
        if opts.toot:
            txt = create_mastodon_txt(artists, opts.period)
            post_toot(settings, txt)
        if opts.skeet:
            txt = create_atproto_txt(artists, opts.period)
            post_skeet(settings, txt)
        if not opts.toot and not opts.skeet:
            txt = create_mastodon_txt(artists, opts.period)
            print(txt)

        return 0

    except CredentialsError as e:
        logger.error(f"Credentials error: {e}")
        print(f"Error: {e}")
        return 2
    except PostingError as e:
        logger.error(f"Posting error: {e}")
        print(f"Error: {e}")
        return 3
    except LastShoutError as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nOperation cancelled by user")
        return 130
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
