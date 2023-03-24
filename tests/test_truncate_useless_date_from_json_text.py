import unittest

from scrapautoscout.scrapper import truncate_useless_data_from_json_text


class test_truncate_useless_date_from_json_text(unittest.TestCase):

    def test_default(self):
        with open('testdata/0a99495b-9bbc-4f0e-acfe-c6930dca8ac7.json') as f:
            json_txt = f.read()

        json_txt_truncated = truncate_useless_data_from_json_text(json_txt)
        print(f'text length truncated by {(len(json_txt_truncated) / len(json_txt) - 1) * 100:.1f}%, '
              f'({len(json_txt) / len(json_txt_truncated):.2f}x times smaller)')

        # This truncatestext length truncated by ~87%, (~7.5x times smaller)
