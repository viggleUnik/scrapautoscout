import unittest
from bs4 import BeautifulSoup

from scrapautoscout.scrapper import get_content_from_all_pages


class test_get_content_from_all_pages(unittest.TestCase):

    def test_default(self):
        pages = get_content_from_all_pages('https://www.autoscout24.com/lst?', max_pages=20)
        self.assertTrue(len(pages) > 0)
        self.assertTrue(isinstance(pages[0], BeautifulSoup))
        # execution time 106.433s
        # - requests.get: 67%
        # - get_valid_proxies_multithreading(): 31%
