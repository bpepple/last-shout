""" Setup file for last-shout """
from setuptools import find_packages, setup
from last_shout import VERSION

setup(
    name="last-shout",
    version=VERSION,
    description="A program to post Last.fm statistics to Twitter and/or Mastodon",
    author="Brian Pepple",
    author_email="bdpepple@gmail.com",
    license="GPLv3",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=["pylast", "python-twitter"],
    entry_points={"console_scripts": ["last-shout=last_shout.main:main"]},
)
