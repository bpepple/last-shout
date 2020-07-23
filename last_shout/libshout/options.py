""" Function to make the parser """
import argparse

from last_shout import VERSION


def create_parser():
    """ Function creating the parser """
    parser = argparse.ArgumentParser(
        description="A program to post last.fm statistics"
        + " to Twitter and/or Mastodon.",
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
        "-n", "--number", type=int, default=10, help="Number of last.fm top artists",
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
    parser.add_argument("--consumer-key", help="Twitter consumer key")
    parser.add_argument("--consumer-secret", help="Twitter consumer secret")
    parser.add_argument("--access-key", help="Twitter access token key")
    parser.add_argument("--access-secret", help="Twitter access secret")
    parser.add_argument(
        "--set-twitter",
        help="Set Twitter credentials",
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
        "--version",
        action="version",
        version="%(prog)s {}".format(VERSION),
        help="Show the version number and exit",
    )

    return parser
