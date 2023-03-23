import unittest

from scrapautoscout.scrapper import find_ids_left_to_extract_local


class test_find_ids_left_to_extract_local(unittest.TestCase):

    def test_default(self):
        ids = find_ids_left_to_extract_local()
        print(f'found {len(ids)} IDs')
        self.assertTrue(len(ids) > 0)
