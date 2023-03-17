import os
import requests  # for making standard html requests
from bs4 import BeautifulSoup  # magical tool for parsing html data
import concurrent.futures
from typing import List
import random
from time import sleep
import logging

from scrapautoscout import config

log = logging.getLogger(os.path.basename(__file__))


def get_raw_proxies_from_url(proxies_url='https://free-proxy-list.net/'):
    raw_proxies = []
    try:
        response = requests.get(proxies_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table table-striped table-bordered')
        if response.status_code == 200:
            for row in table.tbody.find_all('tr'):
                columns = row.find_all('td')
                if columns is not None:
                    ip = columns[0].text.strip()
                    port = columns[1].text.strip()
                    raw_proxies.append(f'{ip}:{port}')
    except:
        return raw_proxies

    return raw_proxies


def extract_response_for_given_ip(proxy, url_for_checks='https://httpbin.org/ip', timeout=2):
    try:
        response = requests.get(url=url_for_checks,
                                headers={'User-Agent': random.choice(config.USER_AGENTS)},
                                proxies={'http': proxy, 'https': proxy},
                                timeout=timeout)
        if response.status_code == 200:
            return proxy
        else:
            return None
    except:
        return None


def get_valid_proxies_multithreading() -> List[str]:
    """ scrape proxy list from site https://free-proxy-list.net/"""

    raw_proxies = []
    n_trials = 0

    while not len(raw_proxies) > 0:
        n_trials += 1
        log.debug(f"attempt={n_trials}: get_raw_proxies_from_url(proxies_url='https://free-proxy-list.net/')")
        raw_proxies = get_raw_proxies_from_url()
        if len(raw_proxies) == 0:
            sleep(10)  # sleep after each failed trial

    log.debug(f'{len(raw_proxies)} raw proxies extracted, now validating...')

    valid_proxies = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for res in executor.map(extract_response_for_given_ip, raw_proxies):
            if res is not None:
                valid_proxies.append(res)

    log.debug(f'{len(valid_proxies)} proxies were validated')

    return valid_proxies

