import unittest

from scrapautoscout.scrapper import main_extract_json_txt_for_all_known_ids


class test_main_extract_json_txt_for_all_known_ids(unittest.TestCase):

    def test_local(self):
        main_extract_json_txt_for_all_known_ids(location='local', chunk_size=100)

    def test_s3(self):
        main_extract_json_txt_for_all_known_ids(location='s3')


