import unittest

from scrapper import get_all_article_ids_forloop


class TestGetAllArticleIDs(unittest.TestCase):
    def test_default(self):
        ids = get_all_article_ids_forloop(
            max_results=5000,
            makers=['audi', 'bmw'],
            years=[1999, 2022],
            price_ranges=[[2000, 5000], [20_000, 50_000]],
            max_pages=1
        )
        self.assertTrue(len(ids) > 0)
