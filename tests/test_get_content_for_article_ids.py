import unittest
from bs4 import BeautifulSoup

from scrapautoscout.scrapper import get_all_article_ids, get_content_for_article_ids, get_json_txt_from_article, \
    save_json_txt
from scrapautoscout.config import config

config.setup()


class test_get_content_for_article_ids(unittest.TestCase):

    def test_default(self):
        ids = get_all_article_ids(makers=['corvette'], max_results=99999)
        print(f'found {len(ids)} IDs')
        articles = get_content_for_article_ids(ids=ids)
        print(f'extracted {len(articles)} articles')
        self.assertTrue(len(articles) / len(ids) > 0.9)
        self.assertTrue(all([isinstance(p, BeautifulSoup) for p in articles.values()]))

    def test_some_known_ids(self):
        ids = [
            '973b5e20-3d9e-455c-b5e0-1a23de1eb6c5',
            '65909b58-0cea-41c5-a2d0-33e75a8ea89f',
            '9073108e-e294-4db9-9287-f610e6a3916e',
            '47424e00-f32c-42a6-862b-c8085759955d'
        ]
        contents = get_content_for_article_ids(ids)
        for id_article, content_article in contents.items():
            json_txt = get_json_txt_from_article(content_article)
            save_json_txt(json_txt=json_txt, id_article=id_article, location='local')
