""" Test for the project settings """
import tempfile
from unittest import TestCase, main

from last_shout.libshout.settings import LastShoutSettings


class TestSettings(TestCase):
    """Some simple tests of the project settings"""

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.config = LastShoutSettings(config_dir=self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_lastfm_credentials(self):
        """Test lastfm credentials settings"""
        user = "test"
        access_key = "123456789041d6db1442edf362e17a83"
        # Save the test config file
        self.config.last_user = user
        self.config.last_access_key = access_key
        self.config.save()

        # Now load that file and verify the contents
        new_config = LastShoutSettings(config_dir=self.tmp_dir.name)
        self.assertEqual(new_config.last_user, user)
        self.assertEqual(new_config.last_access_key, access_key)

    def test_mastodon_credentials(self):
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

        result = LastShoutSettings(config_dir=self.tmp_dir.name)
        self.assertEqual(result.mastodon_client_id, client_id)
        self.assertEqual(result.mastodon_client_secret, client_secret)
        self.assertEqual(result.mastodon_user_token, user_token)
        self.assertEqual(result.mastodon_api_base_url, api_base_url)


if __name__ == "__main__":
    main()
