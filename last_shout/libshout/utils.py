""" Various utilities """

from datetime import datetime

from atproto import client_utils
from atproto_client.utils import TextBuilder
from pylast import TopItem

MUSICAL_NOTE = "\u266A"


def periods_to_string(period: str) -> str:
    """Converts a time period code to a user-friendly string."""
    period_map = {
        "overall": "All-Time",
        "7day": "Weekly",
        "1month": "Monthly",
        "3month": "Quarterly",
        "6month": "Semi-Annual",
        "12month": str(datetime.now().year),
    }
    return period_map.get(period, "")


def _format_artists(artists: list[TopItem]) -> str:
    """
    Formats a list of artists into a comma-separated string with
    an ampersand before the last artist.
    """
    if not artists:
        return ""
    total = len(artists)
    artist_strings = [f"{artist.item.name} ({artist.weight})" for artist in artists]
    if total > 1:
        artist_strings[-1] = (
            f"& {artist_strings[-1]}"  # prepend with ampersand if more than one artist
        )
    return ", ".join(artist_strings)


def create_mastodon_txt(artists: list[TopItem], period: str) -> str:
    """Creates a Mastodon post string with the list of top artists."""
    if not artists:
        return ""
    total = len(artists)
    header = f"{MUSICAL_NOTE} My {periods_to_string(period)} Top {total} #lastfm artists: "
    return f"{header}{_format_artists(artists)}"


def create_atproto_txt(artists: list[TopItem], period: str) -> TextBuilder | None:
    """Creates an AT Protocol post with the list of top artists."""
    if not artists:
        return None
    total = len(artists)
    txt_builder = (
        client_utils.TextBuilder()
        .text(f"{MUSICAL_NOTE} My {periods_to_string(period)} Top {total} ")
        .tag("#lastfm", "lastfm")
        .text(" artists: ")
    )
    return txt_builder.text(_format_artists(artists))
