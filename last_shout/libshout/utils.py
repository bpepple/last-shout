"""Various utilities with improved type safety and error handling."""

from datetime import datetime
from typing import Dict, List, Optional

from atproto import client_utils
from atproto_client.utils import TextBuilder
from pylast import TopItem

MUSICAL_NOTE = "\u266A"

# Constants for better maintainability
PERIOD_MAP: Dict[str, str] = {
    "overall": "All-Time",
    "7day": "Weekly",
    "1month": "Monthly",
    "3month": "Quarterly",
    "6month": "Semi-Annual",
    "12month": str(datetime.now().year),
}


def periods_to_string(period: str) -> str:
    """
    Convert a time period code to a user-friendly string.

    Args:
        period: Time period code (e.g., '7day', '1month')

    Returns:
        User-friendly string representation of the period

    Raises:
        ValueError: If period is not recognized
    """
    if not isinstance(period, str):
        raise TypeError("Period must be a string")

    if not period:
        raise ValueError("Period cannot be empty")

    result = PERIOD_MAP.get(period)
    if result is None:
        valid_periods = ", ".join(PERIOD_MAP.keys())
        raise ValueError(f"Unknown period '{period}'. Valid periods: {valid_periods}")

    return result


def _format_artists(artists: List[TopItem]) -> str:
    """
    Format a list of artists into a comma-separated string with
    an ampersand before the last artist.

    Args:
        artists: List of TopItem objects representing artists

    Returns:
        Formatted string of artists with play counts

    Raises:
        TypeError: If artists is not a list or contains invalid items
    """
    if not isinstance(artists, list):
        raise TypeError("Artists must be a list")

    if not artists:
        return ""

    try:
        artist_strings = []
        for artist in artists:
            if not hasattr(artist, "item") or not hasattr(artist.item, "name"):
                raise ValueError("Invalid artist object structure")
            if not hasattr(artist, "weight"):
                raise ValueError("Artist missing weight attribute")

            name = str(artist.item.name).strip()
            weight = str(artist.weight).strip()

            if not name:
                continue  # Skip artists with empty names

            artist_strings.append(f"{name} ({weight})")

        if not artist_strings:
            return ""

        # Add ampersand before last artist if more than one
        if len(artist_strings) > 1:
            artist_strings[-1] = f"& {artist_strings[-1]}"

        return ", ".join(artist_strings)

    except (AttributeError, TypeError) as e:
        raise ValueError(f"Invalid artist data structure: {e}") from e


def create_mastodon_txt(artists: List[TopItem], period: str) -> str:
    """
    Create a Mastodon post string with the list of top artists.

    Args:
        artists: List of TopItem objects representing artists
        period: Time period code

    Returns:
        Formatted Mastodon post text

    Raises:
        ValueError: If period is invalid or artists data is malformed
        TypeError: If arguments are of wrong type
    """
    if not isinstance(artists, list):
        raise TypeError("Artists must be a list")

    if not artists:
        return ""

    try:
        period_string = periods_to_string(period)
        formatted_artists = _format_artists(artists)

        if not formatted_artists:
            return ""

        total = len([a for a in artists if hasattr(a, "item") and hasattr(a.item, "name")])

        header = f"{MUSICAL_NOTE} My {period_string} Top {total} #lastfm artists: "
        return f"{header}{formatted_artists}"

    except (ValueError, TypeError):
        raise
    except Exception as e:
        raise ValueError(f"Failed to create Mastodon text: {e}") from e


def create_atproto_txt(artists: List[TopItem], period: str) -> Optional[TextBuilder]:
    """
    Create an AT Protocol post with the list of top artists.

    Args:
        artists: List of TopItem objects representing artists
        period: Time period code

    Returns:
        TextBuilder object for AT Protocol post, or None if no valid artists

    Raises:
        ValueError: If period is invalid or artists data is malformed
        TypeError: If arguments are of wrong type
    """
    if not isinstance(artists, list):
        raise TypeError("Artists must be a list")

    if not artists:
        return None

    try:
        period_string = periods_to_string(period)
        formatted_artists = _format_artists(artists)

        if not formatted_artists:
            return None

        total = len([a for a in artists if hasattr(a, "item") and hasattr(a.item, "name")])

        txt_builder = (
            client_utils.TextBuilder()
            .text(f"{MUSICAL_NOTE} My {period_string} Top {total} ")
            .tag("#lastfm", "lastfm")
            .text(" artists: ")
        )

        return txt_builder.text(formatted_artists)

    except (ValueError, TypeError):
        raise
    except Exception as e:
        raise ValueError(f"Failed to create AT Protocol text: {e}") from e


def validate_period(period: str) -> bool:
    """
    Validate if a period string is supported.

    Args:
        period: Time period code to validate

    Returns:
        True if period is valid, False otherwise
    """
    if not isinstance(period, str):
        return False
    return period in PERIOD_MAP


def get_supported_periods() -> List[str]:
    """
    Get list of supported time periods.

    Returns:
        List of supported period codes
    """
    return list(PERIOD_MAP.keys())


def sanitize_text_for_social_media(text: str, max_length: int = 280) -> str:
    """
    Sanitize text for social media posting.

    Args:
        text: Text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text within length limits

    Raises:
        TypeError: If text is not a string
        ValueError: If max_length is not positive
    """
    if not isinstance(text, str):
        raise TypeError("Text must be a string")

    if not isinstance(max_length, int) or max_length <= 0:
        raise ValueError("Max length must be a positive integer")

    # Remove excessive whitespace
    text = " ".join(text.split())

    # Truncate if necessary
    if len(text) > max_length:
        text = text[: max_length - 3] + "..."

    return text
