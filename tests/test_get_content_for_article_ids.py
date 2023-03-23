import unittest
from bs4 import BeautifulSoup

from scrapautoscout.scrapper import get_all_article_ids, get_content_for_article_ids


class test_get_content_for_article_ids(unittest.TestCase):

    def test_default(self):
        ids = get_all_article_ids(makers=['corvette'], max_results=99999)
        print(f'found {len(ids)} IDs')
        articles = get_content_for_article_ids(ids=ids)
        print(f'extracted {len(articles)} articles')
        self.assertTrue(len(articles) / len(ids) > 0.9)
        self.assertTrue(all([isinstance(p, BeautifulSoup) for p in articles.values()]))
