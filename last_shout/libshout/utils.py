""" Various utilities """

import datetime

from pylast import TopItem

MUSICAL_NOTE = "\u266A"


def periods_to_string(period: str) -> str:
    """Function to convert time period setting to string value"""
    now = datetime.datetime.now()
    switcher = {
        "overall": "All-Time",
        "7day": "Weekly",
        "1month": "Monthly",
        "3month": "Quarterly",
        "6month": "Semi-Annual",
        "12month": str(now.year),
    }

    return switcher.get(period, " ")


# TODO: Add function to truncate tweet if it's length is greater than 280 characters.


def create_music_stats(artists: list[TopItem], period: str) -> str:
    """
    Function to convert Last.fm result to a string
    that will be posted to Twitter
    """
    if not artists:
        return ""
    total = len(artists)
    txt = f"{MUSICAL_NOTE} My {periods_to_string(period)} Top {total} #lastfm artists: "

    for count, artist in enumerate(artists, 1):
        txt += f"{artist.item.name} ({artist.weight})"
        if count < total - 1:
            txt += ", "
        elif count == total - 1:
            txt += " & "

    return txt
