import unittest

from scrapper import get_content_from_all_pages



class TestGetContentFromAllPages(unittest.TestCase):

    class TestComposeSearchUrl(unittest.TestCase):
        def test_default(self):
            ids = get_content_from_all_pages('https://www.autoscout24.com/lst?')
            self.assertTrue(len(ids) > 0)


