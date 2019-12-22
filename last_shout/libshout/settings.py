"""Class to handle project settings"""
import configparser
import os
import platform


class LastShoutSettings:
    """Class to handle project settings"""

    @staticmethod
    def get_settings_folder():
        """Method to determine where the users settings should be saved"""
        if platform.system() == "Windows":
            folder = os.path.join(os.environ["APPDATA"], "LastShout")
        else:
            folder = os.path.join(os.path.expanduser("~"), ".LastShout")

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
        # self.mastodon_client_id = ""
        # self.mastodon_client_secret = ""
        # self.mastodon_access_token = ""
        # self.mastodon_api_base_url = ""

    def __init__(self, config_dir=None):
        self.settings_file = ""
        self.folder = ""
        self.set_default_values()

        self.config = configparser.ConfigParser()
        self.folder = config_dir or LastShoutSettings.get_settings_folder()

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.settings_file = os.path.join(self.folder, "settings.ini")

        # Write the config file if it doesn't exist
        if not os.path.exists(self.settings_file):
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

    def save(self):
        """ Method to save user's settings """
        if not self.config.has_section("last_fm"):
            self.config.add_section("last_fm")

        if not self.config.has_section("twitter"):
            self.config.add_section("twitter")

        # if not self.config.has_section("mastodon"):
        #     self.config.add_section("mastodon")

        self.config["last_fm"]["user"] = self.last_user
        self.config["last_fm"]["access_key"] = self.last_access_key

        self.config["twitter"]["consumer_key"] = self.consumer_key
        self.config["twitter"]["consumer_secret"] = self.consumer_secret
        self.config["twitter"]["access_key"] = self.access_key
        self.config["twitter"]["access_secret"] = self.access_secret

        # self.config["mastodon"]["client_id"] = self.mastodon_client_id
        # self.config["mastodon"]["client_secret"] = self.mastodon_client_secret
        # self.config["mastodon"]["access_token"] = self.mastodon_access_token
        # self.config["mastodon"]["api_base_url"] = self.mastodon_api_base_url

        with open(self.settings_file, "w") as configfile:
            self.config.write(configfile)
