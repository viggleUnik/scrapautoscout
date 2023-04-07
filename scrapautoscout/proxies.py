import os
import requests  # for making standard html requests
from bs4 import BeautifulSoup  # magical tool for parsing html data
import concurrent.futures
from typing import List
import random
from time import sleep
import logging
import time
import json

from scrapautoscout.config import config

log = logging.getLogger(os.path.basename(__file__))


def get_raw_proxies_from_url(proxies_url='https://free-proxy-list.net/') -> List[str]:
    raw_proxies = []
    try:
        response = requests.get(proxies_url)
        soup = BeautifulSoup(response.content, 'html.parser')
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
        response = requests.get(
            url=url_for_checks,
            headers={'User-Agent': random.choice(config.USER_AGENTS)},
            proxies={'http': proxy, 'https': proxy},
            timeout=timeout
        )
        if response.status_code == 200:
            return proxy
        else:
            return None
    except:
        return None


def file_age_sec(filepath):
    return time.time() - os.path.getmtime(filepath)


def get_valid_proxies_multithreading(max_workers=100, cache_age_sec=300) -> List[str]:
    """ scrape proxy list from site https://free-proxy-list.net/"""
    log.debug(f'start get_valid_proxies_multithreading()...')

    if config.DIR_CACHE is None:
        config.DIR_CACHE = config.FOLDER_CACHE
        os.makedirs(config.DIR_CACHE, exist_ok=True)

    # load from local cache if available
    filepathcache = f'{config.DIR_CACHE}/proxies.json'
    exists_and_not_old = os.path.exists(filepathcache) and file_age_sec(filepathcache) < cache_age_sec
    if exists_and_not_old:
        with open(filepathcache) as f:
            proxies = json.load(f)
        log.debug(f'loaded {len(proxies)} proxies from local cache, will not extract new proxies yet')
        return proxies

    raw_proxies = []
    n_trials = 0
    max_trials = 10

    while not len(raw_proxies) > 0:
        raw_proxies = get_raw_proxies_from_url()

        if len(raw_proxies) == 0:
            sleep(n_trials * 30)  # sleep after each failed trial

        n_trials += 1
        if n_trials > max_trials:
            log.debug(f"get_raw_proxies_from_url('https://free-proxy-list.net/') failed after {n_trials} attempts")
            return []

    log.debug(f'{len(raw_proxies)} raw proxies extracted, now validating...')

    proxies = []
    n_trials = 0

    while len(proxies) < 10:

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for res in executor.map(extract_response_for_given_ip, raw_proxies):
                if res is not None and res not in proxies:
                    proxies.append(res)

        if n_trials > 5:
            break

    log.debug(f'{len(proxies)} proxies were validated')

    # save to cache
    with open(filepathcache, 'w') as f:
        json.dump(proxies, f, indent=2)

    return proxies

