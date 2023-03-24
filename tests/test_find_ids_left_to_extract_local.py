import unittest

from scrapautoscout.scrapper import find_ids_left_to_extract


class test_find_ids_left_to_extract(unittest.TestCase):

    def test_local(self):
        ids = find_ids_left_to_extract(location='local')
        print(f'found {len(ids)} IDs')
        self.assertTrue(len(ids) > 0)

    def test_s3(self):
        ids = find_ids_left_to_extract(location='s3')
        print(f'found {len(ids)} IDs')
        self.assertTrue(len(ids) > 0)
