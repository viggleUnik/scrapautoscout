import unittest
from bs4 import BeautifulSoup

from scrapautoscout.scrapper import get_content_from_all_pages_parallel


class test_get_content_from_all_pages(unittest.TestCase):

    def test_default(self):
        pages = get_content_from_all_pages_parallel('https://www.autoscout24.com/lst?', max_pages=20)
        self.assertEqual(len(pages), 20)
        self.assertTrue(all([isinstance(p, BeautifulSoup) for p in pages]))
        # execution time: ~26sec (-75% from 106.433sec, or 4x faster)
        # - requests.get: 70%  (18sec, ~1sec/page)
        # - get_valid_proxies_multithreading(): 30% (8sec, called 1 time)
