==========
Last-Shout
==========


.. image:: https://img.shields.io/pypi/v/last-shout.svg
    :target: https://pypi.org/project/last-shout/

.. image:: https://img.shields.io/pypi/pyversions/last-shout.svg
    :target: https://pypi.org/project/last-shout/

.. image:: https://codecov.io/gh/bpepple/last-shout/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/bpepple/last-shout
    :alt: Code coverage Status

.. image:: https://travis-ci.org/bpepple/last-shout.svg?branch=master
    :target: https://travis-ci.org/bpepple/last-shout

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Quick Description
-----------------

A command line tool to tweet a user's top artist statistics from Last.fm to Twitter.

Installation
------------

PyPi
~~~~

Install it yourself:

.. code:: bash

  $ pip install --user last-shout

GitHub
~~~~~~

Installing the latest version from Github:

.. code:: bash

  $ git clone https://github.com/bpepple/last-shout.git
  $ cd last-shout
  $ python3 setup.py install

Getting started
---------------

In order to use Last-Shout, you need at a minimum to get authentication keys for Twitter_ and Last.fm_.

- To get the necessary authenticaton keys for **Twitter**, refer to the documentation here_.

- To get the necessary authentication keys for **Last.fm**, refer to their documentation_.

.. _Twitter: https://twitter.com

.. _Last.fm: https://www.last.fm

.. _here: https://python-twitter.readthedocs.io/en/latest/getting_started.html

.. _documentation: https://python-twitter.readthedocs.io/en/latest/getting_started.html

Help
----

::

  usage: last-shout [-h] [-u USER] [--last-access-key LAST_ACCESS_KEY]
                    [--set-lastfm] [-n NUMBER] [-p PERIOD] [-t]
                    [--consumer-key CONSUMER_KEY]
                    [--consumer-secret CONSUMER_SECRET]
                    [--access-key ACCESS_KEY] [--access-secret ACCESS_SECRET]
                    [--set-twitter] [--version]

  A program to post last.fm statistics to Twitter and/or Mastodon.

  optional arguments:
    -h, --help            show this help message and exit
    -u USER, --user USER  Last.fm username (default: None)
    --last-access-key LAST_ACCESS_KEY
                          Last.fm access key (default: None)
    --set-lastfm          Set Last.fm credentials (default: False)
    -n NUMBER, --number NUMBER
                          Number of last.fm top artists (default: 10)
    -p PERIOD, --period PERIOD
                          The time period over which to retrieve top artists.
                          Options are: overall | 7day | 1month | 3month | 6month
                          | 12month (default: 7day)
    -t, --tweet           Post Last.fm stats to Twitter (default: False)
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
