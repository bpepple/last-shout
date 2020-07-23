""" Setup file for last-shout """
from setuptools import find_packages, setup
from last_shout import VERSION

setup(
    name="last-shout",
    version=VERSION,
    description="A program to post Last.fm statistics to Twitter and/or Mastodon",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="Brian Pepple",
    author_email="bdpepple@gmail.com",
    url="https://github.com/bpepple/last-shout",
    license="GPLv3",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.6",
    install_requires=["pylast", "python-twitter", "mastodon-py"],
    entry_points={"console_scripts": ["last-shout=last_shout.main:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Topic :: Other/Nonlisted Topic",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords=["lastfm", "twitter", "python", "music", "mastodon"],
)
