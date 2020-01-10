""" Various utilites """
import datetime

MUSICAL_NOTE = "\u266A"


def periods_to_string(period):
    """ Function to convert time period setting to string value """
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


def build_twitter_string(artists, period):
    """
    Function to convert Last.fm result to a string
    that will be posted to Twitter
    """
    total = len(artists)
    txt = f"{MUSICAL_NOTE} My {periods_to_string(period)} Top {total} #lastfm artists: "

    for count, artist in enumerate(artists, 1):
        txt += f"{artist.item.name} ({artist.weight})"
        if count < total - 1:
            txt += ", "
        elif count == total - 1:
            txt += " & "

    return txt
