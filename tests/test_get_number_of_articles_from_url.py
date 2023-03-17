import unittest

from scrapautoscout.scrapper import get_numbers_of_articles_from_url, compose_search_url


class test_get_all_ids_for_search_url(unittest.TestCase):

    def test_default(self):
        url = compose_search_url(maker='BMW', fregfrom=1981, fregto=1982, priceto=10_000)
        n_ids = get_numbers_of_articles_from_url(url)
        self.assertTrue(n_ids > 0)
        print(f'n_ids={n_ids}')
