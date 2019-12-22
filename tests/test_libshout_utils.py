""" Test for the project utilities """
from unittest import TestCase, main

from last_shout.libshout.utils import periods_to_string


class TestUtilities(TestCase):
    """ Some basic tests """

    def test_periods_to_string(self):
        result = periods_to_string("7day")
        self.assertEqual(result, "Weekly")


if __name__ == "__main__":
    main()
