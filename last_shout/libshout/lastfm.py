""" Function to users top artist from Last.fm """

import pylast


def get_top_artist(
    last_access_key: str, username: str, number: int, period: str
) -> list[pylast.TopItem]:
    """Simple function returning the users top artists"""
    network = pylast.LastFMNetwork(last_access_key)
    user = network.get_user(username)
    return user.get_top_artists(period=period, limit=number)
