"""Class to handle project settings"""

import configparser
import platform
from os import environ
from pathlib import Path, PurePath

from xdg.BaseDirectory import save_config_path


class LastShoutSettings:
    """Class to handle project settings"""

    @staticmethod
    def get_settings_folder() -> Path:
        """Method to determine where the users settings should be saved"""

        if platform.system() != "Windows":
            return Path(save_config_path("last-shout"))

        windows_path = PurePath(environ["APPDATA"]).joinpath("LastShout")
        return Path(windows_path)

    def __init__(self: "LastShoutSettings", config_dir: str | None = None) -> None:
        """Method to set default values as empty"""
        # Last.fm credentials
        self.last_user: str = ""
        self.last_access_key: str = ""

        # Mastodon credentials
        self.mastodon_client_id: str = ""
        self.mastodon_client_secret: str = ""
        self.mastodon_user_token: str = ""
        self.mastodon_api_base_url: str = ""

        # Bluesky credentials
        self.bluesky_handle: str = ""
        self.bluesky_password: str = ""

        self.config: configparser.ConfigParser = configparser.RawConfigParser()
        if config_dir:
            self.folder = Path(config_dir)
        else:
            self.folder = LastShoutSettings.get_settings_folder()

        if not self.folder.is_dir():
            self.folder.mkdir(parents=True)

        self.settings_file = self.folder.joinpath("settings.ini")

        # Write the config file if it doesn't exist
        if not self.settings_file.is_file():
            self.save()
        else:
            self.load()

    def load(self: "LastShoutSettings") -> None:
        """Method to retrieve user's settings"""
        self.config.read(self.settings_file)

        if self.config.has_option("last_fm", "user"):
            self.last_user = self.config["last_fm"]["user"]

        if self.config.has_option("last_fm", "access_key"):
            self.last_access_key = self.config["last_fm"]["access_key"]

        if self.config.has_option("mastodon", "client_id"):
            self.mastodon_client_id = self.config["mastodon"]["client_id"]

        if self.config.has_option("mastodon", "client_secret"):
            self.mastodon_client_secret = self.config["mastodon"]["client_secret"]

        if self.config.has_option("mastodon", "user_token"):
            self.mastodon_user_token = self.config["mastodon"]["user_token"]

        if self.config.has_option("mastodon", "api_base_url"):
            self.mastodon_api_base_url = self.config["mastodon"]["api_base_url"]

        if self.config.has_option("bluesky", "handle"):
            self.bluesky_handle = self.config["bluesky"]["handle"]

        if self.config.has_option("bluesky", "password"):
            self.bluesky_password = self.config["bluesky"]["password"]

    def save(self: "LastShoutSettings") -> None:
        """Method to save user's settings"""
        if not self.config.has_section("last_fm"):
            self.config.add_section("last_fm")

        if not self.config.has_section("mastodon"):
            self.config.add_section("mastodon")

        if not self.config.has_section("bluesky"):
            self.config.add_section("bluesky")

        self.config["last_fm"]["user"] = self.last_user
        self.config["last_fm"]["access_key"] = self.last_access_key

        self.config["mastodon"]["client_id"] = self.mastodon_client_id
        self.config["mastodon"]["client_secret"] = self.mastodon_client_secret
        self.config["mastodon"]["user_token"] = self.mastodon_user_token
        self.config["mastodon"]["api_base_url"] = self.mastodon_api_base_url

        self.config["bluesky"]["handle"] = self.bluesky_handle
        self.config["bluesky"]["password"] = self.bluesky_password

        with self.settings_file.open(mode="w") as configfile:
            self.config.write(configfile)
