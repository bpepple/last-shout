""" Test for the project utilities """
from unittest import TestCase, main

from last_shout.libshout.utils import periods_to_string


class TestUtilities(TestCase):
    """Some basic tests"""

    def test_periods_to_string(self: "TestUtilities") -> None:
        result = periods_to_string("7day")
        assert result == "Weekly"


if __name__ == "__main__":
    main()
