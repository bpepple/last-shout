""" Function to make the parser """

import argparse

from last_shout import __version__


def create_parser():
    """Function creating the parser"""
    parser = argparse.ArgumentParser(
        description="A program to post last.fm statistics" + " to Twitter and/or Mastodon.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--user", help="Last.fm username")
    parser.add_argument("--last-access-key", help="Last.fm access key")
    parser.add_argument(
        "--set-lastfm",
        help="Set Last.fm credentials",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=10,
        help="Number of last.fm top artists",
    )
    parser.add_argument(
        "-p",
        "--period",
        default="7day",
        help="The time period over which to retrieve top artists.\n"
        + "Options are:\n"
        + "overall | 7day | 1month | 3month | 6month | 12month",
    )
    parser.add_argument(
        "-t",
        "--tweet",
        help="Post Last.fm stats to Twitter",
        action="store_true",
        default=False,
    )
    parser.add_argument("--bluesky-handle", help="Bluesky handle")
    parser.add_argument("--bluesky-password", help="Bluesky password")
    parser.add_argument(
        "--set-bluesky",
        help="Set Bluesky credentials",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--create-mastodon-app",
        help="Create mastodon application",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--create-mastodon-user",
        help="Create Mastodon user token",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--toot",
        help="Post Last.fm stats to Mastodon",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--skeet",
        help="Post Last.fm stats to Bluesky",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version number and exit",
    )

    return parser
