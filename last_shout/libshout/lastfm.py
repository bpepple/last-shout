"""Function to get users top artists from Last.fm with improved error handling."""

import logging
from typing import List, Optional

import pylast

logger = logging.getLogger(__name__)


class LastFMError(Exception):
    """Base exception for Last.fm related errors."""

    pass


class AuthenticationError(LastFMError):
    """Raised when Last.fm authentication fails."""

    pass


class NetworkError(LastFMError):
    """Raised when network communication with Last.fm fails."""

    pass


class UserNotFoundError(LastFMError):
    """Raised when the specified user is not found."""

    pass


def validate_period(period: str) -> bool:
    """
    Validate if the provided period is supported by Last.fm.

    Args:
        period: Time period string

    Returns:
        True if period is valid, False otherwise
    """
    valid_periods = {"overall", "7day", "1month", "3month", "6month", "12month"}
    return isinstance(period, str) and period in valid_periods


def validate_number(number: int) -> bool:
    """
    Validate if the number of artists requested is reasonable.

    Args:
        number: Number of artists to retrieve

    Returns:
        True if number is valid, False otherwise
    """
    return isinstance(number, int) and 1 <= number <= 1000


def get_top_artist(
    last_access_key: str, username: str, number: int, period: str
) -> List[pylast.TopItem]:
    """
    Get the user's top artists from Last.fm with comprehensive error handling.

    Args:
        last_access_key: Last.fm API access key
        username: Last.fm username
        number: Number of artists to retrieve (1-1000)
        period: Time period ('overall', '7day', '1month', '3month', '6month', '12month')

    Returns:
        List of TopItem objects representing the user's top artists

    Raises:
        LastFMError: Base exception for Last.fm related errors
        AuthenticationError: If API key is invalid
        UserNotFoundError: If username doesn't exist
        NetworkError: If network communication fails
        ValueError: If parameters are invalid
        TypeError: If parameters are wrong type
    """
    # Input validation
    if not isinstance(last_access_key, str):
        raise TypeError("last_access_key must be a string")

    if not isinstance(username, str):
        raise TypeError("username must be a string")

    if not isinstance(number, int):
        raise TypeError("number must be an integer")

    if not isinstance(period, str):
        raise TypeError("period must be a string")

    # Validate parameters
    if not last_access_key.strip():
        raise ValueError("last_access_key cannot be empty")

    if not username.strip():
        raise ValueError("username cannot be empty")

    if not validate_number(number):
        raise ValueError("number must be between 1 and 1000")

    if not validate_period(period):
        valid_periods = "overall, 7day, 1month, 3month, 6month, 12month"
        raise ValueError(f"Invalid period '{period}'. Valid periods: {valid_periods}")

    try:
        # Create Last.fm network connection
        logger.debug(f"Connecting to Last.fm for user '{username}'")
        network = pylast.LastFMNetwork(api_key=last_access_key.strip())

        # Get user object
        user = network.get_user(username.strip())

        # Verify user exists by trying to get basic info
        try:
            user.get_playcount()
        except pylast.WSError as e:
            if "User not found" in str(e) or "Invalid user" in str(e):
                raise UserNotFoundError(f"Last.fm user '{username}' not found") from e
            raise

        # Get top artists
        logger.debug(f"Fetching top {number} artists for period '{period}'")
        top_artists = user.get_top_artists(period=period, limit=number)

        logger.info(f"Successfully retrieved {len(top_artists)} artists for user '{username}'")
        return top_artists

    except pylast.NetworkError as e:
        logger.error(f"Network error communicating with Last.fm: {e}")
        raise NetworkError(f"Failed to connect to Last.fm: {e}") from e

    except pylast.WSError as e:
        error_msg = str(e).lower()

        if "invalid api key" in error_msg or "unauthorized" in error_msg:
            logger.error("Invalid Last.fm API key")
            raise AuthenticationError("Invalid Last.fm API key") from e
        elif "user not found" in error_msg or "invalid user" in error_msg:
            logger.error(f"Last.fm user '{username}' not found")
            raise UserNotFoundError(f"Last.fm user '{username}' not found") from e
        else:
            logger.error(f"Last.fm Web Service error: {e}")
            raise LastFMError(f"Last.fm service error: {e}") from e

    except Exception as e:
        logger.exception(f"Unexpected error getting Last.fm data: {e}")
        raise LastFMError(f"Unexpected error retrieving Last.fm data: {e}") from e


def get_user_info(last_access_key: str, username: str) -> Optional[pylast.User]:
    """
    Get basic user information from Last.fm.

    Args:
        last_access_key: Last.fm API access key
        username: Last.fm username

    Returns:
        User object if found, None if not found

    Raises:
        LastFMError: If there's an error accessing Last.fm
        AuthenticationError: If API key is invalid
    """
    if not isinstance(last_access_key, str) or not last_access_key.strip():
        raise ValueError("last_access_key must be a non-empty string")

    if not isinstance(username, str) or not username.strip():
        raise ValueError("username must be a non-empty string")

    try:
        network = pylast.LastFMNetwork(api_key=last_access_key.strip())
        user = network.get_user(username.strip())

        # Test if user exists
        user.get_playcount()
        return user

    except pylast.WSError as e:
        error_msg = str(e).lower()

        if "invalid api key" in error_msg:
            raise AuthenticationError("Invalid Last.fm API key") from e
        elif "user not found" in error_msg:
            return None
        else:
            raise LastFMError(f"Last.fm service error: {e}") from e

    except Exception as e:
        raise LastFMError(f"Unexpected error: {e}") from e


def validate_credentials(last_access_key: str, username: str) -> bool:
    """
    Validate Last.fm credentials by attempting to access user data.

    Args:
        last_access_key: Last.fm API access key
        username: Last.fm username

    Returns:
        True if credentials are valid, False otherwise
    """
    try:
        user_info = get_user_info(last_access_key, username)
        return user_info is not None
    except (LastFMError, ValueError, TypeError):
        return False
