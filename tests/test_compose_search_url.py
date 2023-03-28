import unittest

from scrapautoscout.scrapper import compose_search_url


class test_compose_search_url(unittest.TestCase):

    def test_default(self):
        url = compose_search_url()
        self.assertEqual('https://www.autoscout24.com/lst?', url)

    def test_maker_provided(self):
        url = compose_search_url(maker='BMW')
        self.assertEqual('https://www.autoscout24.com/lst/bmw?', url)

    def test_maker_with_space_provided(self):
        url = compose_search_url(maker='Alfa Romeo')
        self.assertEqual('https://www.autoscout24.com/lst/alfa-romeo?', url)

    def test_prices_provided(self):
        url = compose_search_url(pricefrom=1000, priceto=10000)
        self.assertEqual('https://www.autoscout24.com/lst?pricefrom=1000&priceto=10000', url)

    def test_maker_prices_provided(self):
        url = compose_search_url(maker='BMW', pricefrom=1000, priceto=10000)
        self.assertEqual('https://www.autoscout24.com/lst/bmw?pricefrom=1000&priceto=10000', url)

    def test_maker_years_provided(self):
        url = compose_search_url(maker='BMW', fregfrom=1992, fregto=2000)
        self.assertEqual('https://www.autoscout24.com/lst/bmw?fregfrom=1992&fregto=2000', url)

    def test_maker_years_price_provided(self):
        url = compose_search_url(maker='BMW', fregfrom=1992, fregto=2000, pricefrom=1000, priceto=10000)
        self.assertEqual('https://www.autoscout24.com/lst/bmw?fregfrom=1992&fregto=2000&pricefrom=1000&priceto=10000', url)

    def test_maker_adage_provided(self):
        url = compose_search_url(maker='BMW', adage=1)
        self.assertEqual('https://www.autoscout24.com/lst/bmw?adage=1', url)

    def test_maker_adage_years_provided(self):
        url = compose_search_url(maker='BMW', fregfrom=2020, fregto=2023, adage=1)
        self.assertEqual('https://www.autoscout24.com/lst/bmw?adage=1&fregfrom=2020&fregto=2023', url)

    def test_maker_adage_price_provided(self):
        url = compose_search_url(maker='BMW', adage=1, pricefrom=10000, priceto=20000)
        self.assertEqual('https://www.autoscout24.com/lst/bmw?adage=1&pricefrom=10000&priceto=20000', url)
