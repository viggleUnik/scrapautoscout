import os
import requests  # for making standard html requests
from bs4 import BeautifulSoup  # magical tool for parsing html data
import concurrent.futures
from typing import List
import random
import logging

from scrapautoscout import config


log = logging.getLogger(os.path.basename(__file__))


def get_raw_proxies_from_url(proxies_url='https://free-proxy-list.net/'):
    raw_proxies = []
    response = requests.get(proxies_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='table table-striped table-bordered')

    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')
        if columns is not None:
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            raw_proxies.append(f'{ip}:{port}')

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
    # scrape proxy list from site
    raw_proxies = get_raw_proxies_from_url()
    valid_proxies = []

    # tests proxies
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for res in executor.map(extract_response_for_given_ip, raw_proxies):
            if res is not None:
                valid_proxies.append(res)

    log.debug(f'found {len(valid_proxies)} valid proxies')
    return valid_proxies

