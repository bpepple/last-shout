""" Function to make the parser """
import argparse

from .. import VERSION


def create_parser():
    """ Function creating the parser """
    parser = argparse.ArgumentParser(
        description="A program to post last.fm statistics to Twitter and/or Mastodon.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--user", help="Last.fm username")
    parser.add_argument(
        "-n", "--number", type=int, help="Number of last.fm top artists (default is 10)"
    )
    parser.add_argument(
        "-p",
        "--period",
        default="7day",
        help="The time period over which to retrieve top artists.\n"
        + "Options are:\n"
        + "overall | 7day | 1month | 3month | 6month | 12month\n"
        + "(default is 7day)",
    )
    parser.add_argument("--consumer-key", help="Twitter consumer key")
    parser.add_argument("--consumer-secret", help="Twitter consumer secret")
    parser.add_argument("--access-key", help="Twitter access token key")
    parser.add_argument("--access-secret", help="Twitter access secret")
    parser.add_argument("--last-access-key", help="Last.fm access key")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(VERSION),
        help="Show the version number and exit",
    )

    return parser
