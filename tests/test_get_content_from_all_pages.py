import unittest
from bs4 import BeautifulSoup

from scrapautoscout.scrapper import get_content_from_all_pages


class test_get_content_from_all_pages(unittest.TestCase):

    def test_default(self):
        pages = get_content_from_all_pages('https://www.autoscout24.com/lst?', max_pages=20)
        self.assertTrue(len(pages) == 20)
        self.assertTrue(all([isinstance(p, BeautifulSoup) for p in pages]))
        # execution time 106.433sec
        # - requests.get: 67%  (71sec, ~3.55sec/page)
        # - get_valid_proxies_multithreading(): 31%  (30sec, called 1 time)

    def test_default_without_proxies_without_sleep(self):
        pages = get_content_from_all_pages('https://www.autoscout24.com/lst?', max_pages=20, use_proxy=False, sleep_btw_reqs=0)
        self.assertTrue(len(pages) == 20)
        self.assertTrue(all([isinstance(p, BeautifulSoup) for p in pages]))
        # execution time 18sec (without sleeping between requests)
        # - requests.get: 99%  (~1sec/page)

    def test_default_without_proxies_with_sleep_5s(self):
        pages = get_content_from_all_pages('https://www.autoscout24.com/lst?', max_pages=20, use_proxy=False, sleep_btw_reqs=5)
        self.assertTrue(len(pages) == 20)
        self.assertTrue(all([isinstance(p, BeautifulSoup) for p in pages]))
        # execution time 100sec (with sleep=5sec between requests)
        # - requests.get: 99%  (~5sec/page)
