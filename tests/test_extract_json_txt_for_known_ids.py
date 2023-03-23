import unittest

from scrapautoscout.scrapper import extract_json_txt_for_known_ids


class test_extract_json_txt_for_known_ids(unittest.TestCase):

    def test_local(self):
        extract_json_txt_for_known_ids(location='local', chunk_size=100)
