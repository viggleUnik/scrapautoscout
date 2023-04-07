import unittest

from scrapautoscout.scrapper import get_all_article_ids
from scrapautoscout.config import config

config.setup()


class test_get_all_article_ids(unittest.TestCase):

    def test_aston_martin(self):
        ids = get_all_article_ids(makers=['Aston Martin'])
        print(f'{len(ids)} found')
        self.assertTrue(len(ids) > 0)
        # Version 1:
        # - execution time 330.482s
        # - 888 found
        # - get_all_ids_for_search_url() called: 4 times
        # - get_raw_proxies_from_url() called: 4 times
        # - Failed to get content for url: 21 times

        # Version 2: use get_valid_proxies_multithreading(max_workers=100):
        # - execution time 245.049s (-25%)
        # - 888 found
        # - get_all_ids_for_search_url() called: 4 times
        # - get_raw_proxies_from_url() called: 4 times
        # - Failed to get content for url: 23 times

        # Version 3: use get_valid_proxies_multithreading(max_workers=100), use global PROXIES:
        # - execution time 199.322s (-18%)
        # - 888 found
        # - get_all_ids_for_search_url() called: 4 times
        # - get_raw_proxies_from_url() called: 1 time
        # - Failed to get content for url: 10 times

        # retrieved_counts:
        # {
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\"}": 960,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 1980, \"fregto\": 2023}": 888,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 2002, \"fregto\": 2023}": 828,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 2013, \"fregto\": 2023}": 499,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 2019, \"fregto\": 2023}": 324,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 2013, \"fregto\": 2018}": 175,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 2002, \"fregto\": 2012}": 329,
        #   "{\"adage\": 365, \"maker\": \"Aston Martin\", \"fregfrom\": 1980, \"fregto\": 2001}": 60
        # }

    def test_dodge(self):
        ids = get_all_article_ids(makers=['dodge'])
        print(f'{len(ids)} found')
        self.assertTrue(len(ids) > 0)

    # makers=['dodge']:
    # execution time: 15min 50sec ( Ver 3: 497.932s => -47%)
    # retrieved: 2909 IDs
    # called get_all_ids_for_search_url() 13 times (~60sec/call)
    # called get_raw_proxies_from_url() 13 times (~30sec/call)
    # retrieved_counts:
    # {
    #   "{\"adage\": 365, \"maker\": \"dodge\"}": 4219,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 1980, \"fregto\": 2023}": 2901,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2002, \"fregto\": 2023}": 2809,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2013, \"fregto\": 2023}": 2270,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2023}": 1455,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2022, \"fregto\": 2023}": 727,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023}": 416,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 1000000}": 416,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500001, \"priceto\": 1000000}": 0,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 500000}": 416,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 250001, \"priceto\": 500000}": 2,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 250000}": 414,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 125001, \"priceto\": 250000}": 20,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 125000}": 394,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2022, \"fregto\": 2022}": 311,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2021}": 729,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2021, \"fregto\": 2021}": 210,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2020}": 519,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2020, \"fregto\": 2020}": 203,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2019}": 316,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2013, \"fregto\": 2018}": 815,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2016, \"fregto\": 2018}": 575,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2018, \"fregto\": 2018}": 238,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2016, \"fregto\": 2017}": 337,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2013, \"fregto\": 2015}": 240,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2002, \"fregto\": 2012}": 540,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2008, \"fregto\": 2012}": 346,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2002, \"fregto\": 2007}": 194,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 1980, \"fregto\": 2001}": 92
    # }

    def test_cadillac_s3(self):
        ids = get_all_article_ids(makers=['Cadillac'], cache_location='s3')
        print(f'{len(ids)} found')
        self.assertTrue(len(ids) > 0)

