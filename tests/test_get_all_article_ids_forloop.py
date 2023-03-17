import unittest

from scrapautoscout.scrapper import get_all_article_ids_forloop


class test_get_all_article_ids_forloop(unittest.TestCase):

    def test_default(self):
        ids = get_all_article_ids_forloop(
            makers=['audi', 'bmw'],
            years=[1999, 2022],
            price_ranges=[[2000, 5000], [20_000, 50_000]],
        )
        print(f'{len(ids)} found')
        self.assertTrue(len(ids) > 0)
