""" Test for the main """

import tempfile
from unittest import TestCase, main

from last_shout.libshout.settings import LastShoutSettings
from last_shout.main import (
    has_lastfm_credentials,
    has_mastodon_app_credentials,
    has_mastodon_user_credentials,
)


class TestMain(TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.config = LastShoutSettings(config_dir=self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_lastfm_with_credentials(self):
        """Test lastfm credentials settings"""
        user = "test"
        access_key = "123456789041d6db1442edf362e17a83"
        # Save the test config file
        self.config.last_user = user
        self.config.last_access_key = access_key
        self.config.save()

        # Now load that file and verify the contents
        tmp_settings = LastShoutSettings(config_dir=self.tmp_dir.name)
        result = has_lastfm_credentials(tmp_settings)
        self.assertTrue(result)

    def test_lastfm_without_credentials(self):
        access_key = "123456789041d6db1442edf362e17a83"
        # Save the test config file without adding the user
        self.config.last_access_key = access_key
        self.config.save()

        # Now load that file and verify the contents
        tmp_settings = LastShoutSettings(config_dir=self.tmp_dir.name)
        result = has_lastfm_credentials(tmp_settings)
        self.assertFalse(result)





    def test_mastodon_with_credentials(self):
        """Test mastodon credentials settings"""
        client_id = "H4to3LMKNmZ6a6pRGNKgvgej1TGKI66y6PEckNkfU5U"
        client_secret = "KDkEHbCD8kMi36BspWErfOxopoS9UQNVrjL4o6lwxqc"
        user_token = "123abc456789"
        api_base_url = "https://mastodon.social"

        self.config.mastodon_client_id = client_id
        self.config.mastodon_client_secret = client_secret
        self.config.mastodon_user_token = user_token
        self.config.mastodon_api_base_url = api_base_url
        self.config.save()

        tmp_settings = LastShoutSettings(config_dir=self.tmp_dir.name)
        result = has_mastodon_app_credentials(tmp_settings)
        self.assertTrue(result)

    def test_mastodon_without_credentials(self):
        """Test mastodon credentials settings"""
        client_id = "H4to3LMKNmZ6a6pRGNKgvgej1TGKI66y6PEckNkfU5U"
        client_secret = "KDkEHbCD8kMi36BspWErfOxopoS9UQNVrjL4o6lwxqc"

        # Don't add the base url instance
        self.config.mastodon_client_id = client_id
        self.config.mastodon_client_secret = client_secret
        self.config.save()

        tmp_settings = LastShoutSettings(config_dir=self.tmp_dir.name)
        result = has_mastodon_app_credentials(tmp_settings)
        self.assertFalse(result)

    def test_mastodon_user_with_credentials(self):
        """Test mastodon credentials settings"""
        user_token = "123abc456789"

        self.config.mastodon_user_token = user_token
        self.config.save()

        tmp_settings = LastShoutSettings(config_dir=self.tmp_dir.name)
        result = has_mastodon_user_credentials(tmp_settings)
        self.assertTrue(result)

    def test_mastodon_user_without_credentials(self):
        """Test mastodon credentials settings"""
        client_id = "H4to3LMKNmZ6a6pRGNKgvgej1TGKI66y6PEckNkfU5U"

        # Don't save the user token
        self.config.mastodon_client_id = client_id
        self.config.save()

        tmp_settings = LastShoutSettings(config_dir=self.tmp_dir.name)
        result = has_mastodon_user_credentials(tmp_settings)
        self.assertFalse(result)


if __name__ == "__main__":
    main()
