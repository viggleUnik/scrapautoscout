import unittest

from scrapautoscout.scrapper import find_all_json_files_with_ids
from scrapautoscout.config import config

config.setup()

class test_find_all_json_files_with_ids(unittest.TestCase):

    def test_s3(self):
        files_json = find_all_json_files_with_ids(location='s3')
        self.assertTrue(len(files_json) > 0)
        print('\n'.join(files_json))

    def test_local(self):
        files_json = find_all_json_files_with_ids()
        self.assertTrue(len(files_json) > 0)
        print('\n'.join(files_json))
