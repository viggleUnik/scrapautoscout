import os.path
import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from typing import Dict, List, Tuple
import logging
import base64
import hashlib
import random
import boto3
import math

from scrapautoscout import config
from scrapautoscout.proxies import get_valid_proxies_multithreading

log = logging.getLogger(os.path.basename(__file__))


def compose_search_url(
        search_url: str = config.SITE_URL,
        maker: str = None,
        fregfrom: int = None,
        fregto: int = None,
        pricefrom: int = None,
        priceto: int = None,
        adage: int = None,
        **kwargs,
) -> str:

    """
    Compose url with given parameters for filtering
    examples returned:
    - https://www.autoscout24.com/lst/bmw?fregfrom=2020&fregto=2020&pricefrom=20000&priceto=23000&page=2
    - https://www.autoscout24.com/lst/bmw?fregfrom=2000&fregto=2000&pricefrom=500&priceto=2000
    """

    if not search_url.endswith('/lst'):
        search_url = f'{search_url}/lst'

    if maker is not None:
        maker = maker.lower().replace(' ', '-')
        search_url = f'{search_url}/{maker}?'

    if not search_url.endswith('?'):
        search_url = f'{search_url}?'

    filters = {
        'adage': adage,
        'fregfrom': fregfrom,
        'fregto': fregto,
        'pricefrom': pricefrom,
        'priceto': priceto,
    }

    filters.update(kwargs)

    # filter fields which are not None
    filters = {k: v for k, v in filters.items() if v is not None}
    filters_str_pairs = [f'{k}={v}' for k, v in filters.items()]
    filters_compounded = '&'.join(filters_str_pairs)
    search_url = f'{search_url}{filters_compounded}'

    return search_url


def get_content_from_all_pages(
        search_url: str,
        headers: Dict = None,
        max_pages: int = config.MAX_PAGES,
) -> List[BeautifulSoup]:
    """
    Get content of all pages for a given search
    :param search_url: search url, e.g. https://www.autoscout24.com/lst/bmw?fregfrom=2000&fregto=2000&pricefrom=500&priceto=2000
    :param headers: headers
    :param max_pages: max pages to explore, e.g. 20 allowed
    :return: list of BeautifulSoup objects (one for each page)
    """

    if headers is None:
        headers = {'User-Agent': random.choice(config.USER_AGENTS)}

    pages = []
    # get valid proxies for rotation
    proxies_valid_ips = get_valid_proxies_multithreading()

    for i in range(1, max_pages + 1):
        found = False
        while not found:
            # case proxies list is empty, we go further only if we have at least 3 valid proxies
            if len(proxies_valid_ips) == 0:
                proxies_min = False
                while not proxies_min:
                    proxies_valid_ips = get_valid_proxies_multithreading()
                    if len(proxies_valid_ips) > 3:
                        proxies_min = True

            url_page = f'{search_url}&page={i}'
            proxy_ip = random.choice(proxies_valid_ips)
            proxy = {'http': proxy_ip, 'https': proxy_ip}

            try:
                page = requests.get(url=url_page, headers=headers, proxies=proxy, timeout=5)
                if page.status_code == 200:
                    soup = BeautifulSoup(page.text, 'html.parser')
                    pages.append(soup)
                    found = True
                else:
                    proxies_valid_ips.remove(proxy_ip)
            except requests.exceptions.RequestException as e:
                proxies_valid_ips.remove(proxy_ip)
                log.error(f'error {e}')
            pass
    log.info(f'Content For: {search_url} Extracted!')
    return pages


def get_article_ids(pages: List[BeautifulSoup], n_articles_max: int = None) -> List[str]:
    """
    Get all articles IDs from a list of pages
    :param pages: list of BeautifulSoup objects
    :n_articles_max: maximum number of articles to extract
    :return: list of article IDs
    """
    article_ids = []

    for page in pages:
        articles = page.find_all('article')
        for article in articles:
            article_ids.append(article.get('id'))
            if n_articles_max is not None and len(article_ids) >= n_articles_max:
                return article_ids

    return article_ids


def get_hash_from_string(s: str) -> str:
    md5bytes = hashlib.md5(s.encode()).digest()
    hash_str = base64.urlsafe_b64encode(md5bytes).decode('ascii')
    hash_str = ''.join(c for c in hash_str if c.isalnum())
    return hash_str


def get_all_ids_for_search_url(
        search_url: str,
        n_search_results: int = None,
        cache_folder: str = 'get_all_ids_for_search_url'
    ):

    log.debug(f'running get_all_ids_for_search_url(search_url={search_url})')

    # cache dir and json file with ids
    dir_cache = f'{config.DIR_CACHE}/{cache_folder}'
    os.makedirs(dir_cache, exist_ok=True)
    path_file = f'{dir_cache}/{get_hash_from_string(search_url)}.json'

    # load from local cache if available
    if os.path.exists(path_file):
        with open(path_file) as f:
            ids = json.load(f)
        log.debug(f'loaded {len(ids)} from local cache')
        return ids

    if n_search_results is None:
        n_search_results = get_numbers_of_articles_from_url(search_url)

    nr_of_pages = calculate_nr_of_pages(nr_results=n_search_results)

    list_bs = get_content_from_all_pages(search_url, max_pages=nr_of_pages)
    ids = get_article_ids(list_bs, n_search_results)

    # save to cache
    with open(path_file, 'w') as f:
        json.dump(ids, f, indent=2)

    return ids


def trunc_error_msg(e, max_chars=200):
    return (str(e)[:max_chars] + '...') if len(str(e)) > max_chars else str(e)


def get_json_data_from_article(
        article_id: str,
        site_url: str = config.SITE_URL,
        headers: Dict = None,
        proxy: Dict = None,
):

    if headers is None:
        headers = {'User-Agent': random.choice(config.USER_AGENTS)}

    article_url = f'{site_url}/offers/{article_id}'
    json_text = None
    status_code = None
    try:
        page = requests.get(article_url, headers=headers, proxies=proxy, timeout=5)
        status_code = page.status_code
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        json_text = soup.select_one('script[id="__NEXT_DATA__"]').text
    except requests.exceptions.RequestException as e:
        log.debug(f'Failed to get json data for {article_url} with error: {trunc_error_msg(e)}')

    return json_text, status_code


def get_numbers_of_articles_from_url(url: str, max_trials=5, sleep_after_fail=30) -> int:
    sleep(random.randint(1, 3))
    n_trials = 0
    while n_trials < max_trials:
        try:
            user_agent = random.choice(config.USER_AGENTS)
            page = requests.get(url, headers={'User-Agent': user_agent})
            soup = BeautifulSoup(page.text, 'html.parser')
            json_text = soup.select_one('script[id="__NEXT_DATA__"]').text
            obj = json.loads(json_text)
            n_offers = obj['props']['pageProps']['numberOfResults']
            return int(n_offers)
        except requests.exceptions.RequestException as e:
            log.error(f'Failed to get the number of offers for url {url} on attempt={n_trials} with error: '
                      f'{trunc_error_msg(e)}')
            n_trials += 1
            sleep(n_trials * sleep_after_fail)  # sleep after failed trial, each time by more

    log.error(f'Failed to get the number of offers for url {url} after {max_trials} attempts.')
    return -1


def calculate_nr_of_pages(
        nr_results: int,
        res_per_page: int = config.MAX_RESULTS_PER_PAGE,
        max_pages: int = config.MAX_PAGES
    ) -> int:
    return min(math.ceil(float(nr_results) / res_per_page), max_pages)


def get_all_article_ids(
        makers: List[str] = config.MAKERS,
        year_range: Tuple[int, int] = config.YEAR_RANGE,
        price_range: Tuple[int, int] = config.PRICE_RANGE,
        adage: int = config.ADAGE,
        max_results: int = config.MAX_RESULTS,
        max_retrievals: int = None,
        price_step = 500,
):
    """
    Get all car ids and save them to cache folder
    :param max_results: when to stop narrowing the filter, if number of search results is less or equal,
        no further narrowing is performed, default: 400 results (maximum retrievable per search)
    :param max_retrievals: maximum allowed number of IDs retrievals
    """
    price_step = math.ceil(price_step / 100) * 100  # make sure is a multiple of 100

    all_ids = []
    retrieved_counts = {}
    n_retrievals = 0

    # initiate stack
    # - initiate with empty filter, no parameters specified
    stack = [{}]

    # - initiate with 'adage', if 'adage' was specified
    if adage is not None:
        pars = stack.pop()
        pars_with_adage = {**pars, **{'adage': adage}}
        stack.append(pars_with_adage)

    # - initiate with makers, if makers were specified (usually, the makers are specified)
    if makers is not None and len(makers) > 0:
        pars = stack.pop()
        for maker in reversed(makers):
            pars_with_maker = {**pars, **{'maker': maker}}
            stack.append(pars_with_maker)

    # perform depth first search, narrow filter if too many results found (>max_results)
    while len(stack) > 0:
        if max_retrievals is not None and n_retrievals > max_retrievals:
            break

        log.debug('\nretrieved_counts:\n' + json.dumps(retrieved_counts, indent=2))
        # log.debug('\nstack:\n' + json.dumps(stack, indent=2))

        pars = stack.pop()
        pars_as_key = json.dumps(pars)

        # check if this set of parameters was retrieved before
        n_results = retrieved_counts.get(pars_as_key, None)
        if n_results is not None:
            continue  # if it was already retrieved, then skip to not repeat the same work

        # check how many results are found when searching with this set for parameters
        search_url = compose_search_url(**pars)
        n_results = get_numbers_of_articles_from_url(search_url)
        retrieved_counts[pars_as_key] = n_results  # record the number of results for this set of parameters

        if n_results <= 0:
            # if -1 (error) or 0 (zero results found), then nothing to do, go to next
            continue
        elif n_results <= max_results:
            # if less than maximum results, retrieve all articles IDs, as we don't want to narrow the filter further
            ids = get_all_ids_for_search_url(search_url, n_results)
            all_ids.extend(ids)
            n_retrievals += 1
        else:
            # if more than max results, there are too many results, we want to narrow the filter and break down
            # the set of results with additional parameters if possible

            # try to be more specific about years
            fregfrom, fregto = pars.get('fregfrom'), pars.get('fregto')
            pars_has_years = fregfrom is not None and fregto is not None
            if not pars_has_years:
                # if params does not have years, add years and append new params to stack
                fregfrom, fregto = year_range
                new_pars = {**pars, **{'fregfrom': fregfrom, 'fregto': fregto}}
                stack.append(new_pars)
                continue
            elif pars_has_years and fregfrom < fregto:
                # if params has years specified and if there is a range between fregfrom and fregto,
                # then divide it at mid-point into 2 new ranges and add new params to stack
                mid = (fregfrom + fregto) // 2
                new_pars_left = {**pars, **{'fregfrom': fregfrom, 'fregto': mid}}
                new_pars_right = {**pars, **{'fregfrom': mid + 1, 'fregto': fregto}}
                stack.append(new_pars_left)
                stack.append(new_pars_right)
                continue

            # try to be more specific about price
            pricefrom, priceto = pars.get('pricefrom'), pars.get('priceto')
            pars_has_prices = pricefrom is not None and priceto is not None
            if not pars_has_prices:
                # if params does not have prices, add prices and append new params to stack
                pricefrom, priceto = price_range
                new_pars = {**pars, **{'pricefrom': pricefrom, 'priceto': priceto}}
                stack.append(new_pars)
                continue
            elif pars_has_prices and (priceto - pricefrom) > price_step:
                # if params has prices and if there is a wide enough range between pricefrom and priceto,
                # then divide it at midpoint into 2 new ranges and add new params to stack
                mid = (pricefrom + priceto) // 2
                mid = math.floor(mid / price_step) * price_step  # round down to price_step
                new_pars_left = {**pars, **{'pricefrom': min(pricefrom, mid), 'priceto': mid}}
                new_pars_right = {**pars, **{'pricefrom': mid + 1, 'priceto': priceto}}
                stack.append(new_pars_left)
                stack.append(new_pars_right)
                continue

            # if the set of parameters could not be narrowed more, then retrieve just the first 400 IDs for this search
            ids = get_all_ids_for_search_url(search_url, n_results)
            all_ids.extend(ids)
            n_retrievals += 1

    return all_ids


def get_all_article_ids_forloop(
        makers: List[str] = config.MAKERS,
        years: List[int] = config.YEARS,
        price_ranges: List[List[int]] = config.PRICE_RANGES,
        max_results: int = config.MAX_RESULTS,
):
    """
    Get all car ids and save them to cache folder
    """

    all_ids = []

    # find results for makers
    for maker in makers:
        # find results for years of registration
        for year in years:
            search_url = compose_search_url(maker=maker, fregfrom=year, fregto=year)
            n_results = get_numbers_of_articles_from_url(search_url)

            if n_results == -1:
                continue  # case when error

            elif n_results == 0:
                continue

            elif n_results < max_results:
                # case when less than 400 results found (max nr of pages explorable via browser)
                ids = get_all_ids_for_search_url(search_url, n_results)
                all_ids.extend(ids)

            elif n_results > max_results:
                # case when more than 400 results found, will narrow the search with price ranges
                for price_from, price_to in price_ranges:
                    search_url = compose_search_url(maker=maker, fregfrom=year, fregto=year,
                                                    pricefrom=price_from, priceto=price_to)
                    n_results = get_numbers_of_articles_from_url(search_url)

                    if n_results == -1:
                        continue

                    elif n_results == 0:
                        continue

                    elif n_results > 0:
                        ids = get_all_ids_for_search_url(search_url, n_results)
                        all_ids.extend(ids)

    return all_ids


def read_ids_json_files_from_cache():
    """Get car ids from cached json files"""

    path_to_json = f'{config.DIR_CACHE}/get_all_ids_for_search_url/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    dir_get_content = f'{config.DIR_CACHE}/get_content_id'
    os.makedirs(dir_get_content, exist_ok=True)

    # file browsing in 'cache/get_all_ids_for_search_url'
    for jfile in json_files:
        with open(path_to_json + jfile, 'r') as file:
            list_ids = json.load(file)

        # creating directory name for each given json file with ids
        dir_name = jfile.replace('.json', '')
        folder_path = os.path.join(dir_get_content, dir_name)
        create_folder_with_jsons_ids(list_ids, folder_path)


def create_folder_with_jsons_ids(car_ids: List[str], folder_path: str):
    """Get car information from site and create folder with jsons"""

    os.makedirs(folder_path, exist_ok=True)

    # get valid proxies for scrapping
    proxies_valid_ips = get_valid_proxies_multithreading()

    for id in car_ids:
        id_file_name = f'{folder_path}/{id}.json'
        # check if id_file exists in folder
        if os.path.exists(id_file_name):
            log.info(f'exists {id}.json')
            continue
        else:
            found = False
            request_try = 0
            while not found:
                # case proxies list is empty, we go further only if we have at least 3 valid proxies
                if len(proxies_valid_ips) == 0:
                    min_valid = False
                    while not min_valid:
                        proxies_valid_ips = get_valid_proxies_multithreading()
                        if len(proxies_valid_ips) > 3:
                            min_valid = True

                # choose randon proxy from list
                proxy_ip = random.choice(proxies_valid_ips)
                proxy = {'http': proxy_ip, 'https': proxy_ip}
                print(f'proxy {proxy}')

                # choose random user agent from stored USER_AGENTS
                user_agent = random.choice(config.USER_AGENTS)
                json_text, status_code = get_json_data_from_article(
                    headers={'User-Agent': user_agent},
                    article_id=id,
                    proxy=proxy)

                # check if request was successful
                if json_text is not None:
                    # create file with car info
                    with open(id_file_name, 'w') as f:
                        json.dump(json_text, f, indent=2)
                    print(f'SUCCESS!')
                    found = True
                else:
                    if request_try == 3:
                        found = True
                        # create an empty json for further verification
                        with open(id_file_name, 'w') as f:
                            json.dump('{}', f, indent=2)
                        request_try = 0

                    elif request_try < 3:
                        request_try += 1
                        proxies_valid_ips.remove(proxy_ip)


def s3_read_ids_json_files_from_cache():
    path_to_json = f'{config.DIR_CACHE}/get_all_ids_for_search_url'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    # Create a session using the default profile
    session = boto3.Session(profile_name='default')

    # file browsing in 'cache/get_all_ids_for_search_url'
    for jfile in json_files:
        with open(f'{path_to_json}/{jfile}', 'r') as file:
            list_ids = json.load(file)

        # creating s3 directory name for each given json file with ids
        dir_name = jfile.replace('.json', '')
        s3_create_folder_with_jsons_ids(car_ids=list_ids, folder_path=dir_name, bucket_name=config.BUCKET,
                                        boto_session=session)


def s3_create_folder_with_jsons_ids(car_ids: List[str], folder_path: str, bucket_name: str,
                                    boto_session: boto3.session.Session):
    # Get car information from site and create folder with jsons

    # Use the session to create an S3 client
    client = boto_session.client('s3')
    folder_response = client.list_objects(Bucket=bucket_name, Prefix=folder_path)

    if 'Contents' not in folder_response:
        # get valid proxies for scrapping
        proxies_valid_ips = get_valid_proxies_multithreading()

        for car_id in car_ids:
            found = False
            request_try = 0

            while not found:
                # case proxies list is empty, we go further only if we have at least 3 valid proxies
                if len(proxies_valid_ips) == 0:
                    min_valid = False
                    while not min_valid:
                        proxies_valid_ips = get_valid_proxies_multithreading()
                        if len(proxies_valid_ips) > 3:
                            min_valid = True

                # choose randon proxy from list
                proxy_ip = random.choice(proxies_valid_ips)
                proxy = {'http': proxy_ip, 'https': proxy_ip}

                # choose random user agent from stored USER_AGENTS
                user_agent = random.choice(config.USER_AGENTS)
                json_text, status_code = get_json_data_from_article(
                    headers={'User-Agent': user_agent},
                    article_id=car_id,
                    proxy=proxy)

                # check if request was successful
                if json_text is not None:
                    # create file with car info
                    key_file_name = f'{folder_path}/{car_id}.json'
                    client.put_object(
                        Bucket=bucket_name,
                        Key=key_file_name,
                        Body=json_text
                    )
                    found = True
                elif status_code == 404:
                    break
                else:
                    # try with another proxy, remove the current bad proxy
                    if request_try < 3:
                        request_try += 1
                        proxies_valid_ips.remove(proxy_ip)
                    else:
                        break  # give up, exit while loop
