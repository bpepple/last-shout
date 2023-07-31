""" Test for the argparser """

from unittest import TestCase, main

from last_shout.libshout import options


class TestOptions(TestCase):
    """Simple tests for argparser"""

    def setUp(self: "TestOptions") -> None:
        self.parser = options.create_parser()

    def test_credentials_options(self: "TestOptions") -> None:
        """Some test for credentials options"""
        parsed = self.parser.parse_args(["--user", "test_user"])
        assert parsed.user == "test_user"

    def test_number_option(self: "TestOptions") -> None:
        """Test to verify the option returns an integer"""
        parsed = self.parser.parse_args(["-n", "5"])
        assert parsed.number == 5

    def test_set_lastfm(self: "TestOptions") -> None:
        """Test setting of last.fm credentials option"""
        parsed = self.parser.parse_args(["--set-lastfm"])
        assert parsed.set_lastfm


if __name__ == "__main__":
    main()
