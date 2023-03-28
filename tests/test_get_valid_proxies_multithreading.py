import unittest

from scrapautoscout.scrapper import get_valid_proxies_multithreading
from scrapautoscout.config import config

config.setup()


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

    def test_difference(self):
        ips_1 = get_valid_proxies_multithreading(max_workers=100, cache_age_sec=0)
        ips_2 = get_valid_proxies_multithreading(max_workers=100, cache_age_sec=0)

        print(set(ips_1).intersection(set(ips_2)))
        print(set(ips_1) - set(ips_2))
        print(set(ips_2) - set(ips_1))
        # {'8.219.176.202:8080', '20.206.106.192:80', '46.4.242.214:1337'}
        # {'81.12.44.197:3129', '193.141.126.54:82', '16.163.217.247:8888'}
        # {'3.24.58.156:3128', '20.111.54.16:80', '35.233.162.87:3100', '43.133.6.40:8081'}
