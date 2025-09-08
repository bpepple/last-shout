"""Class to handle project settings with improved error handling and validation."""

import configparser
import logging
import platform
from os import environ
from pathlib import Path, PurePath
from typing import Optional

from xdg.BaseDirectory import save_config_path

logger = logging.getLogger(__name__)


class SettingsError(Exception):
    """Base exception for settings-related errors."""

    pass


class LastShoutSettings:
    """Class to handle project settings with improved validation and error handling."""

    # Configuration sections and keys
    SECTION_LASTFM = "last_fm"
    SECTION_MASTODON = "mastodon"
    SECTION_BLUESKY = "bluesky"

    CONFIG_FILE_NAME = "settings.ini"
    APP_NAME = "last-shout"
    WINDOWS_APP_NAME = "LastShout"

    @staticmethod
    def get_settings_folder() -> Path:
        """
        Determine where the user's settings should be saved.

        Returns:
            Path to settings directory

        Raises:
            SettingsError: If unable to determine settings path
        """
        try:
            if platform.system() != "Windows":
                return Path(save_config_path(LastShoutSettings.APP_NAME))

            if "APPDATA" not in environ:
                raise SettingsError("APPDATA environment variable not found on Windows")

            windows_path = PurePath(environ["APPDATA"]).joinpath(
                LastShoutSettings.WINDOWS_APP_NAME
            )
            return Path(windows_path)

        except Exception as e:
            raise SettingsError(f"Failed to determine settings folder: {e}") from e

    def __init__(self, config_dir: Optional[str] = None) -> None:
        """
        Initialize settings with default values and load existing configuration.

        Args:
            config_dir: Optional custom configuration directory path

        Raises:
            SettingsError: If settings initialization fails
        """
        # Initialize Last.fm credentials
        self.last_user: str = ""
        self.last_access_key: str = ""

        # Initialize Mastodon credentials
        self.mastodon_client_id: str = ""
        self.mastodon_client_secret: str = ""
        self.mastodon_user_token: str = ""
        self.mastodon_api_base_url: str = ""

        # Initialize Bluesky credentials
        self.bluesky_handle: str = ""
        self.bluesky_password: str = ""

        self.config: configparser.ConfigParser = configparser.RawConfigParser()

        try:
            self.folder = Path(config_dir) if config_dir else self.get_settings_folder()

            # Ensure settings directory exists
            if not self.folder.exists():
                self.folder.mkdir(parents=True, mode=0o700)  # Secure permissions
                logger.info(f"Created settings directory: {self.folder}")

            self.settings_file = self.folder / self.CONFIG_FILE_NAME

            # Load existing settings or create new file
            if self.settings_file.exists():
                self.load()
            else:
                self.save()
                logger.info(f"Created new settings file: {self.settings_file}")

        except Exception as e:
            raise SettingsError(f"Failed to initialize settings: {e}") from e

    def _ensure_sections_exist(self) -> None:
        """Ensure all required configuration sections exist."""
        sections = [self.SECTION_LASTFM, self.SECTION_MASTODON, self.SECTION_BLUESKY]

        for section in sections:
            if not self.config.has_section(section):
                self.config.add_section(section)

    def _validate_config_file(self) -> bool:
        """
        Validate that the configuration file is readable and has expected structure.

        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            if not self.settings_file.exists():
                return False

            if not self.settings_file.is_file():
                logger.warning(f"Settings path exists but is not a file: {self.settings_file}")
                return False

            # Try to read the file
            test_config = configparser.RawConfigParser()
            test_config.read(self.settings_file)

            return True

        except (configparser.Error, PermissionError, OSError) as e:
            logger.error(f"Configuration file validation failed: {e}")
            return False

    def load(self) -> None:
        """
        Load user's settings from configuration file.

        Raises:
            SettingsError: If settings cannot be loaded
        """
        try:
            if not self._validate_config_file():
                raise SettingsError("Invalid or unreadable configuration file")

            self.config.read(self.settings_file, encoding="utf-8")

            # Load Last.fm settings
            if self.config.has_option(self.SECTION_LASTFM, "user"):
                self.last_user = self.config.get(
                    self.SECTION_LASTFM, "user", fallback=""
                ).strip()

            if self.config.has_option(self.SECTION_LASTFM, "access_key"):
                self.last_access_key = self.config.get(
                    self.SECTION_LASTFM, "access_key", fallback=""
                ).strip()

            # Load Mastodon settings
            if self.config.has_option(self.SECTION_MASTODON, "client_id"):
                self.mastodon_client_id = self.config.get(
                    self.SECTION_MASTODON, "client_id", fallback=""
                ).strip()

            if self.config.has_option(self.SECTION_MASTODON, "client_secret"):
                self.mastodon_client_secret = self.config.get(
                    self.SECTION_MASTODON, "client_secret", fallback=""
                ).strip()

            if self.config.has_option(self.SECTION_MASTODON, "user_token"):
                self.mastodon_user_token = self.config.get(
                    self.SECTION_MASTODON, "user_token", fallback=""
                ).strip()

            if self.config.has_option(self.SECTION_MASTODON, "api_base_url"):
                self.mastodon_api_base_url = self.config.get(
                    self.SECTION_MASTODON, "api_base_url", fallback=""
                ).strip()

            # Load Bluesky settings
            if self.config.has_option(self.SECTION_BLUESKY, "handle"):
                self.bluesky_handle = self.config.get(
                    self.SECTION_BLUESKY, "handle", fallback=""
                ).strip()

            if self.config.has_option(self.SECTION_BLUESKY, "password"):
                self.bluesky_password = self.config.get(
                    self.SECTION_BLUESKY, "password", fallback=""
                ).strip()

            logger.debug("Settings loaded successfully")

        except configparser.Error as e:
            raise SettingsError(f"Configuration file parsing error: {e}") from e
        except (PermissionError, OSError) as e:
            raise SettingsError(f"Failed to read settings file: {e}") from e

    def save(self) -> None:
        """
        Save user's settings to configuration file.

        Raises:
            SettingsError: If settings cannot be saved
        """
        try:
            # Ensure all sections exist
            self._ensure_sections_exist()

            # Set Last.fm settings
            self.config.set(self.SECTION_LASTFM, "user", self.last_user)
            self.config.set(self.SECTION_LASTFM, "access_key", self.last_access_key)

            # Set Mastodon settings
            self.config.set(self.SECTION_MASTODON, "client_id", self.mastodon_client_id)
            self.config.set(
                self.SECTION_MASTODON, "client_secret", self.mastodon_client_secret
            )
            self.config.set(self.SECTION_MASTODON, "user_token", self.mastodon_user_token)
            self.config.set(self.SECTION_MASTODON, "api_base_url", self.mastodon_api_base_url)

            # Set Bluesky settings
            self.config.set(self.SECTION_BLUESKY, "handle", self.bluesky_handle)
            self.config.set(self.SECTION_BLUESKY, "password", self.bluesky_password)

            # Write to file with secure permissions
            with self.settings_file.open(mode="w", encoding="utf-8") as configfile:
                self.config.write(configfile)

            # Set secure file permissions (user read/write only)
            self.settings_file.chmod(0o600)

            logger.debug("Settings saved successfully")

        except configparser.Error as e:
            raise SettingsError(f"Configuration writing error: {e}") from e
        except (PermissionError, OSError) as e:
            raise SettingsError(f"Failed to write settings file: {e}") from e

    def clear_lastfm_credentials(self) -> None:
        """Clear Last.fm credentials from settings."""
        self.last_user = ""
        self.last_access_key = ""
        logger.info("Last.fm credentials cleared")

    def clear_mastodon_credentials(self) -> None:
        """Clear Mastodon credentials from settings."""
        self.mastodon_client_id = ""
        self.mastodon_client_secret = ""
        self.mastodon_user_token = ""
        self.mastodon_api_base_url = ""
        logger.info("Mastodon credentials cleared")

    def clear_bluesky_credentials(self) -> None:
        """Clear Bluesky credentials from settings."""
        self.bluesky_handle = ""
        self.bluesky_password = ""
        logger.info("Bluesky credentials cleared")

    def clear_all_credentials(self) -> None:
        """Clear all stored credentials."""
        self.clear_lastfm_credentials()
        self.clear_mastodon_credentials()
        self.clear_bluesky_credentials()
        logger.info("All credentials cleared")

    def has_lastfm_credentials(self) -> bool:
        """Check if Last.fm credentials are configured."""
        return bool(self.last_user and self.last_access_key)

    def has_mastodon_app_credentials(self) -> bool:
        """Check if Mastodon app credentials are configured."""
        return bool(
            self.mastodon_client_id
            and self.mastodon_client_secret
            and self.mastodon_api_base_url
        )

    def has_mastodon_user_credentials(self) -> bool:
        """Check if Mastodon user token is configured."""
        return bool(self.mastodon_user_token)

    def has_bluesky_credentials(self) -> bool:
        """Check if Bluesky credentials are configured."""
        return bool(self.bluesky_handle and self.bluesky_password)

    def __repr__(self) -> str:
        """Return string representation of settings (without sensitive data)."""
        return (
            f"LastShoutSettings("
            f"last_user='{self.last_user}', "
            f"has_last_access_key={bool(self.last_access_key)}, "
            f"mastodon_api_base_url='{self.mastodon_api_base_url}', "
            f"has_mastodon_credentials={self.has_mastodon_app_credentials()}, "
            f"bluesky_handle='{self.bluesky_handle}', "
            f"has_bluesky_credentials={self.has_bluesky_credentials()}"
            f")"
        )
