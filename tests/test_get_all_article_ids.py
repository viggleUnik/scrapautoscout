import unittest

from scrapautoscout.scrapper import get_all_article_ids


class test_get_all_article_ids(unittest.TestCase):

    def test_default(self):
        ids = get_all_article_ids(makers=['dodge'])
        print(f'{len(ids)} found')
        self.assertTrue(len(ids) > 0)

    # makers=['dodge']:
    # execution time: 1018.062s (~19min 28sec)
    # retrieved: 2905 IDs
    # retrieved_counts:
    # {
    #   "{\"adage\": 365, \"maker\": \"dodge\"}": 4225,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 1980, \"fregto\": 2023}": 2906,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2002, \"fregto\": 2023}": 2814,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2013, \"fregto\": 2023}": 2272,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2023}": 1456,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2022, \"fregto\": 2023}": 724,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023}": 414,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 1000000}": 414,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500001, \"priceto\": 1000000}": 0,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 500000}": 414,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 250001, \"priceto\": 500000}": 2,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 250000}": 412,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 125001, \"priceto\": 250000}": 20,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2023, \"fregto\": 2023, \"pricefrom\": 500, \"priceto\": 125000}": 392,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2022, \"fregto\": 2022}": 310,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2021}": 732,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2021, \"fregto\": 2021}": 210,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2020}": 522,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2020, \"fregto\": 2020}": 206,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2019, \"fregto\": 2019}": 316,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2013, \"fregto\": 2018}": 816,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2016, \"fregto\": 2018}": 568,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2018, \"fregto\": 2018}": 233,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2016, \"fregto\": 2017}": 335,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2013, \"fregto\": 2015}": 248,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2002, \"fregto\": 2012}": 541,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2008, \"fregto\": 2012}": 347,
    #   "{\"adage\": 365, \"maker\": \"dodge\", \"fregfrom\": 2002, \"fregto\": 2007}": 194
    # }
