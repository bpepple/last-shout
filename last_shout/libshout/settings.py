"""Class to handle project settings"""
import configparser
import platform
from os import environ
from pathlib import Path


class LastShoutSettings:
    """Class to handle project settings"""

    @staticmethod
    def get_settings_folder():
        """Method to determine where the users settings should be saved"""
        if platform.system() == "Windows":
            folder = Path(environ["APPDATA"]).joinpath("LastShout")
        else:
            folder = Path.home() / ".LastShout"

        return folder

    def set_default_values(self):
        """Method to set default values as empty"""
        # Last.fm credentials
        self.last_user = ""
        self.last_access_key = ""

        # Twitter credentials
        self.consumer_key = ""
        self.consumer_secret = ""
        self.access_key = ""
        self.access_secret = ""

        # Mastodon credentials
        self.mastodon_client_id = ""
        self.mastodon_client_secret = ""
        self.mastodon_user_token = ""
        self.mastodon_api_base_url = ""

    def __init__(self, config_dir=None):
        self.set_default_values()

        self.config = configparser.ConfigParser()
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

    def load(self):
        """ Method to retrieve user's settings """
        self.config.read(self.settings_file)

        if self.config.has_option("last_fm", "user"):
            self.last_user = self.config["last_fm"]["user"]

        if self.config.has_option("last_fm", "access_key"):
            self.last_access_key = self.config["last_fm"]["access_key"]

        if self.config.has_option("twitter", "consumer_key"):
            self.consumer_key = self.config["twitter"]["consumer_key"]

        if self.config.has_option("twitter", "consumer_secret"):
            self.consumer_secret = self.config["twitter"]["consumer_secret"]

        if self.config.has_option("twitter", "access_key"):
            self.access_key = self.config["twitter"]["access_key"]

        if self.config.has_option("twitter", "access_secret"):
            self.access_secret = self.config["twitter"]["access_secret"]

        if self.config.has_option("mastodon", "client_id"):
            self.mastodon_client_id = self.config["mastodon"]["client_id"]

        if self.config.has_option("mastodon", "client_secret"):
            self.mastodon_client_secret = self.config["mastodon"]["client_secret"]

        if self.config.has_option("mastodon", "user_token"):
            self.mastodon_user_token = self.config["mastodon"]["user_token"]

        if self.config.has_option("mastodon", "api_base_url"):
            self.mastodon_api_base_url = self.config["mastodon"]["api_base_url"]

    def save(self):
        """ Method to save user's settings """
        if not self.config.has_section("last_fm"):
            self.config.add_section("last_fm")

        if not self.config.has_section("twitter"):
            self.config.add_section("twitter")

        if not self.config.has_section("mastodon"):
            self.config.add_section("mastodon")

        self.config["last_fm"]["user"] = self.last_user
        self.config["last_fm"]["access_key"] = self.last_access_key

        self.config["twitter"]["consumer_key"] = self.consumer_key
        self.config["twitter"]["consumer_secret"] = self.consumer_secret
        self.config["twitter"]["access_key"] = self.access_key
        self.config["twitter"]["access_secret"] = self.access_secret

        self.config["mastodon"]["client_id"] = self.mastodon_client_id
        self.config["mastodon"]["client_secret"] = self.mastodon_client_secret
        self.config["mastodon"]["user_token"] = self.mastodon_user_token
        self.config["mastodon"]["api_base_url"] = self.mastodon_api_base_url

        with self.settings_file.open(mode="w") as configfile:
            self.config.write(configfile)
