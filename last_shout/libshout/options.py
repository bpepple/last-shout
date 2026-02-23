"""Function to create the command-line argument parser with improved validation."""

import argparse
import sys
from typing import List, Optional

from last_shout import __version__


class ValidationError(Exception):
    """Raised when argument validation fails."""

    pass


def validate_number(value_: str) -> int:
    """
    Validate and convert the number of artists argument.

    Args:
        value_: String value to validate

    Returns:
        Validated integer value

    Raises:
        argparse.ArgumentTypeError: If validation fails
    """
    try:
        num = int(value_)
        if num < 1:
            raise argparse.ArgumentTypeError("Number must be at least 1")
        if num > 1000:
            raise argparse.ArgumentTypeError("Number cannot exceed 1000 (Last.fm limit)")
        return num
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value_}' is not a valid number")


def validate_period(value_: str) -> str:
    """
    Validate the time period argument.

    Args:
        value_: String value to validate

    Returns:
        Validated period string

    Raises:
        argparse.ArgumentTypeError: If validation fails
    """
    valid_periods = {"overall", "7day", "1month", "3month", "6month", "12month"}

    if value_ not in valid_periods:
        valid_list = ", ".join(sorted(valid_periods))
        raise argparse.ArgumentTypeError(
            f"'{value_}' is not a valid period. Choose from: {valid_list}"
        )

    return value_


def validate_url(value_: str) -> str:
    """
    Validate URL format for Mastodon instances.

    Args:
        value_: URL string to validate

    Returns:
        Validated URL string

    Raises:
        argparse.ArgumentTypeError: If URL format is invalid
    """
    if not value_:
        raise argparse.ArgumentTypeError("URL cannot be empty")

    # Add https:// if no scheme provided
    if not value_.startswith(("http://", "https://")):
        value_ = f"https://{value_}"

    # Basic URL validation
    if not value_.startswith(("http://", "https://")):
        raise argparse.ArgumentTypeError("Invalid URL format")

    if len(value_) < 8:  # Minimum reasonable URL length
        raise argparse.ArgumentTypeError("URL too short")

    return value_.rstrip("/")  # Remove trailing slash


class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Custom formatter with improved help text formatting."""

    def _format_action_invocation(self, action):
        """Format action invocation with better alignment."""
        if not action.option_strings:
            (metavar,) = self._metavar_formatter(action, action.dest)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    parts.append(f"{option_string} {args_string}")
            return ", ".join(parts)


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the command-line argument parser with comprehensive validation.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="last-shout",
        description=(
            "A program to post Last.fm statistics to social media platforms. "
            "Share your music listening habits on Twitter, Mastodon, and Bluesky."
        ),
        formatter_class=CustomHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s -u my_username --toot\n"
            "  %(prog)s -n 5 -p 1month --skeet\n"
            "  %(prog)s --set-lastfm\n"
        ),
        add_help=True,
    )

    # Last.fm configuration
    lastfm_group = parser.add_argument_group("Last.fm Configuration")
    lastfm_group.add_argument("-u", "--user", metavar="USERNAME", help="Last.fm username")
    lastfm_group.add_argument("--last-access-key", metavar="KEY", help="Last.fm API access key")
    lastfm_group.add_argument(
        "--set-lastfm",
        action="store_true",
        help="Save Last.fm credentials to configuration file",
    )

    # Statistics configuration
    stats_group = parser.add_argument_group("Statistics Configuration")
    stats_group.add_argument(
        "-n",
        "--number",
        type=validate_number,
        default=10,
        metavar="NUM",
        help="Number of top artists to include (1-1000)",
    )
    stats_group.add_argument(
        "-p",
        "--period",
        type=validate_period,
        default="7day",
        metavar="PERIOD",
        help=(
            "Time period for top artists. Options: overall, 7day, 1month, 3month, 6month, 12month"
        ),
    )

    # Social media posting
    posting_group = parser.add_argument_group("Social Media Posting")
    posting_group.add_argument(
        "-t",
        "--tweet",
        action="store_true",
        help="Post Last.fm statistics to Twitter (deprecated)",
    )
    posting_group.add_argument(
        "--toot", action="store_true", help="Post Last.fm statistics to Mastodon"
    )
    posting_group.add_argument(
        "--skeet", action="store_true", help="Post Last.fm statistics to Bluesky"
    )

    # Mastodon configuration
    mastodon_group = parser.add_argument_group("Mastodon Configuration")
    mastodon_group.add_argument(
        "--create-mastodon-app",
        action="store_true",
        help="Create and register a new Mastodon application",
    )
    mastodon_group.add_argument(
        "--create-mastodon-user",
        action="store_true",
        help="Generate Mastodon user access token",
    )
    mastodon_group.add_argument(
        "--mastodon-instance",
        type=validate_url,
        metavar="URL",
        help="Mastodon instance URL (e.g., https://mastodon.social)",
    )

    # Bluesky configuration
    bluesky_group = parser.add_argument_group("Bluesky Configuration")
    bluesky_group.add_argument(
        "--bluesky-handle", metavar="HANDLE", help="Bluesky handle (e.g., user.bsky.social)"
    )
    bluesky_group.add_argument(
        "--bluesky-password", metavar="PASSWORD", help="Bluesky password or app password"
    )
    bluesky_group.add_argument(
        "--set-bluesky",
        action="store_true",
        help="Save Bluesky credentials to configuration file",
    )

    # General options
    general_group = parser.add_argument_group("General Options")
    general_group.add_argument(
        "--config-dir", metavar="PATH", help="Custom configuration directory path"
    )
    general_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be posted without actually posting",
    )
    general_group.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging output"
    )
    general_group.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version number and exit",
    )

    return parser


def validate_args(args_: argparse.Namespace) -> None:
    """
    Validate argument combinations and dependencies.

    Args:
        args_: Parsed arguments namespace

    Raises:
        ValidationError: If argument validation fails
    """
    # Check for conflicting actions
    setup_actions = [
        args_.create_mastodon_app,
        args_.create_mastodon_user,
        args_.set_lastfm,
        args_.set_bluesky,
    ]

    posting_actions = [args_.toot, args_.skeet, args_.tweet]

    if sum(setup_actions) > 1:
        raise ValidationError("Only one setup action can be performed at a time")

    # If doing setup, don't allow posting
    if any(setup_actions) and any(posting_actions):
        raise ValidationError("Cannot perform setup and posting actions in the same command")

    # Warn about deprecated Twitter option
    if args_.tweet:
        print("Warning: Twitter posting is deprecated and may not work", file=sys.stderr)

    # Check for posting without credentials (will be handled by main logic)
    if args_.toot and not (args_.create_mastodon_app or args_.create_mastodon_user):
        # This will be validated in main() with actual settings
        pass

    if args_.skeet and not args_.set_bluesky:
        # This will be validated in main() with actual settings
        pass


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments with validation.

    Args:
        argv: Optional list of arguments (for testing)

    Returns:
        Parsed and validated arguments namespace

    Raises:
        SystemExit: If parsing fails or validation errors occur
    """
    parser = create_parser()

    try:
        args_ = parser.parse_args(argv)
        validate_args(args_)
        return args_
    except ValidationError as e:
        parser.error(str(e))
    except Exception as e:
        parser.error(f"Argument parsing failed: {e}")
