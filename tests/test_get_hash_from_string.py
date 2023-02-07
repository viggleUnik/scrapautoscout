import unittest

from scrapautoscout.scrapper import get_hash_from_string


class TestGetHashFromString(unittest.TestCase):

    def test_simple(self):
        hash_str = get_hash_from_string('https://www.autoscout24.com/lst')
        self.assertTrue(isinstance(hash_str, str))
        self.assertTrue(0 < len(hash_str) < 100)
        self.assertTrue(hash_str.isalnum())
