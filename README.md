# Last-Shout

[![PyPI - Version](https://img.shields.io/pypi/v/last-shout.svg)](https://pypi.org/project/last-shout/)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/last-shout.svg)](https://pypi.org/project/last-shout/)
[![Pre-Commit](https://img.shields.io/badge/Pre--Commit-Enabled-informational?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

A command line tool to toot a user's top artist statistics from Last.fm to Mastodon.

## Installation

Installing the latest version from Github:

```bash
pipx install last-shout
```

## Getting started

In order to use Last-Shout, you need at a minimum to get authentication keys for [Last.fm](https://www.last.fm) and
Mastodon.

## Help

```bash
 usage: last-shout [-h] [-u USER] [--last-access-key LAST_ACCESS_KEY] [--set-lastfm] [-n NUMBER] [-p PERIOD] [-t] [--bluesky-handle BLUESKY_HANDLE] [--bluesky-password BLUESKY_PASSWORD] [--set-bluesky] [--create-mastodon-app]
                  [--create-mastodon-user] [--toot] [--skeet] [--version]

 A program to post last.fm statistics to Twitter and/or Mastodon.

 options:
  -h, --help            show this help message and exit
  -u, --user USER       Last.fm username (default: None)
  --last-access-key LAST_ACCESS_KEY
                        Last.fm access key (default: None)
  --set-lastfm          Set Last.fm credentials (default: False)
  -n, --number NUMBER   Number of last.fm top artists (default: 10)
  -p, --period PERIOD   The time period over which to retrieve top artists. Options are: overall | 7day | 1month | 3month | 6month | 12month (default: 7day)
  -t, --tweet           Post Last.fm stats to Twitter (default: False)
  --bluesky-handle BLUESKY_HANDLE
                        Bluesky handle (default: None)
  --bluesky-password BLUESKY_PASSWORD
                        Bluesky password (default: None)
  --set-bluesky         Set Bluesky credentials (default: False)
  --create-mastodon-app
                        Create mastodon application (default: False)
  --create-mastodon-user
                        Create Mastodon user token (default: False)
  --toot                Post Last.fm stats to Mastodon (default: False)
  --skeet               Post Last.fm stats to Bluesky (default: False)
  --version             Show the version number and exit
```

## Set Systemd Timer

Once you've set your credentials in the application, most users will want it to run on regular intervals, and if you're
running a Linux distribution with systemd you can set-up a timer to do that.

Start by a systemd unit file for it in `~/.config/systemd/user/last-shout-weekly.service`

```text
[Unit]
Description=Run weekly Last-Shout
After=network.target

[Service]
Type=oneshot
WorkingDirectory=%h
ExecStart=%h/.local/bin/last-shout --toot --skeet

[Install]
WantedBy=default.target
```

Now let's create a time for it in `~/.config/systemd/user/last-shout-weekly.timer`:

```text
[Unit]
Description=Start the Systemd service test.service every 10 minutes

[Timer]
OnCalendar=Fri 11:30
Persistent=true

[Install]
WantedBy=timers.target
```

Then run the following to enable it:

```bash
systemctl --user enable --now last-shout-weekly.timer
```

Then reload the user daemon:

```bash
systemctl --user daemon-reload
```

Now run the following to verify the timer is enabled by running:

```bash
systemctl --user list-timers
```

If everything is alright you should see output similar to this:

```bash
bpepple@faramir:~$ systemctl --user list-timers
NEXT                          LEFT LAST                              PASSED UNIT                         ACTIVATES                     
Tue 2025-01-28 16:53:50 EST    23h Mon 2025-01-27 16:53:50 EST 4min 21s ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Fri 2025-01-31 11:30:00 EST 3 days Fri 2025-01-24 11:30:06 EST            - last-shout-weekly.timer      last-shout-weekly.service
-                                - Mon 2025-01-27 16:50:50 EST     7min ago grub-boot-success.timer      grub-boot-success.service

3 timers listed.

```