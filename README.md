# Last-Shout

## Quick Description

A command line tool to tweet a user's top artist statistics from Last.fm to Twitter.

### Installation

* Coming as soon as the first release is made.

### Getting started

In order to use Last-Shout, you need at a minimum to get authentication keys for [Twitter](https://twitter.com) and [Last.fm](https://www.last.fm).

* To get the necessary authenticaton keys for **Twitter**, refer to the documentation [here](https://python-twitter.readthedocs.io/en/latest/getting_started.html).

* To get the necessary authentication keys for **Last.fm**, refer to their documentation [here](https://www.last.fm/api/).

#### Help

```bash
usage: main.py [-h] [-u USER] [--last-access-key LAST_ACCESS_KEY]
               [--set-lastfm] [-n NUMBER] [-p PERIOD]
               [--consumer-key CONSUMER_KEY]
               [--consumer-secret CONSUMER_SECRET] [--access-key ACCESS_KEY]
               [--access-secret ACCESS_SECRET] [--set-twitter] [--version]

A program to post last.fm statistics to Twitter and/or Mastodon.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Last.fm username (default: None)
  --last-access-key LAST_ACCESS_KEY
                        Last.fm access key (default: None)
  --set-lastfm          Set Last.fm credentials (default: False)
  -n NUMBER, --number NUMBER
                        Number of last.fm top artists (default is 10)
                        (default: 10)
  -p PERIOD, --period PERIOD
                        The time period over which to retrieve top artists.
                        Options are: overall | 7day | 1month | 3month | 6month
                        | 12month (default is 7day) (default: 7day)
  --consumer-key CONSUMER_KEY
                        Twitter consumer key (default: None)
  --consumer-secret CONSUMER_SECRET
                        Twitter consumer secret (default: None)
  --access-key ACCESS_KEY
                        Twitter access token key (default: None)
  --access-secret ACCESS_SECRET
                        Twitter access secret (default: None)
  --set-twitter         Set Twitter credentials (default: False)
  --version             Show the version number and exit
```
