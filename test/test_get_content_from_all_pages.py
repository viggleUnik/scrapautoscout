import unittest
from bs4 import BeautifulSoup

from scrapper import get_content_from_all_pages


class TestGetContentFromAllPages(unittest.TestCase):
    def test_default(self):
        pages = get_content_from_all_pages('https://www.autoscout24.com/lst?')
        self.assertTrue(len(pages) > 0)
        self.assertTrue(isinstance(pages[0], BeautifulSoup))
