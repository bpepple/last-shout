""" Test for the argparser """
import tempfile
from unittest import TestCase, main

from last_shout.libshout import options


class TestOptions(TestCase):
    """ Simple tests for argparser """

    def setUp(self):
        self.parser = options.create_parser()
        self.path = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.path.cleanup()

    def test_credentials_options(self):
        """ Some test for credentials options """
        parsed = self.parser.parse_args(["--user", "test_user",])
        self.assertEqual(parsed.user, "test_user")

    def test_number_option(self):
        """ Test to verify the option returns an integer """
        parsed = self.parser.parse_args(["-n", "5"])
        self.assertEqual(parsed.number, 5)


if __name__ == "__main__":
    main()
