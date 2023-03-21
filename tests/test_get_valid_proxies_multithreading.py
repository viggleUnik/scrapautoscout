import unittest

from scrapautoscout.scrapper import get_valid_proxies_multithreading


class test_get_all_ids_for_search_url(unittest.TestCase):

    def test_default(self):
        ips = get_valid_proxies_multithreading(max_workers=10)
        self.assertTrue(len(ips) > 0)
        print('\n'.join(ips))
        # execution time: 30 sec

    def test_max_workers_100(self):
        ips = get_valid_proxies_multithreading(max_workers=100)
        self.assertTrue(len(ips) > 0)
        print('\n'.join(ips))
        # execution time: 8 sec
