import unittest

from scrapautoscout.scrapper import get_all_ids_for_search_url, compose_search_url
from scrapautoscout.config import config

config.setup()


class test_get_all_ids_for_search_url(unittest.TestCase):

    def test_local(self):
        url = compose_search_url(maker='BMW', fregfrom=1981, fregto=1982, priceto=10_000)
        ids = get_all_ids_for_search_url(search_url=url, cache_location='local')
        self.assertTrue(len(ids) > 0)
        print('\n'.join(ids))

    def test_s3(self):
        url = compose_search_url(maker='BMW', fregfrom=1981, fregto=1982, priceto=10_000)
        ids = get_all_ids_for_search_url(search_url=url, cache_location='s3')
        self.assertTrue(len(ids) > 0)
        print('\n'.join(ids))
