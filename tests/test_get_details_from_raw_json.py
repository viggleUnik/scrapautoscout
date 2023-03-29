import json
import unittest

from scrapautoscout.scrapper import truncate_useless_data_from_json_text
from scrapautoscout.transform import get_details_from_raw_json


class test_get_details_from_raw_json(unittest.TestCase):

    def test_default(self):
        ids = [
            '0a99495b-9bbc-4f0e-acfe-c6930dca8ac7',
            '973b5e20-3d9e-455c-b5e0-1a23de1eb6c5',
            '65909b58-0cea-41c5-a2d0-33e75a8ea89f',
            '9073108e-e294-4db9-9287-f610e6a3916e',
            '47424e00-f32c-42a6-862b-c8085759955d',
        ]
        l_dicts = []

        for id_ in ids:
            with open(f'testdata/{id_}.json') as f:
                json_txt = f.read()
            json_txt_truncated = truncate_useless_data_from_json_text(json_txt)
            row_as_dict = get_details_from_raw_json(json_txt_truncated)
            self.assertTrue(isinstance(row_as_dict, dict))
            l_dicts.append(row_as_dict)

        print(json.dumps(l_dicts, indent=2))
