import copy
import os.path
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import Dict, List, Tuple
import logging
import random
import boto3
import math
import concurrent.futures
import glob
from tqdm import tqdm


from scrapautoscout.config import config
from scrapautoscout.proxies import get_valid_proxies_multithreading
from scrapautoscout.utils import format_seconds, get_hash_from_string, trunc_msg, update_nested_dict, \
    remove_none_from_dict

log = logging.getLogger(os.path.basename(__file__))

PROXIES = []


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


def send_get_request(url, headers, proxies=None, timeout=5):
    msg_proxy = f'via proxy {list(proxies.values())[0]}' if proxies is not None else ''
    try:
        page = requests.get(url=url, headers=headers, proxies=proxies, timeout=timeout)
        if page.status_code == 200:
            return {'status': 200, 'content': BeautifulSoup(page.content, 'html.parser')}
        else:
            log.debug(f'Failed to get content for url: {url} {msg_proxy} with status: {page.status_code}, reason: {page.reason}')
            return {'status': page.status_code, 'content': None}
    except requests.exceptions.RequestException as e:
        log.debug(f'Failed to get content for url: {url} {msg_proxy} with error: {trunc_msg(e)}')
        return {'status': None, 'content': None}


def get_request_params_from_url(url: str, use_header=True, use_proxy=True, timeout=5):
    global PROXIES

    params = {'url': url, 'timeout': timeout}

    if use_header:
        params['headers'] = {'User-Agent': random.choice(config.USER_AGENTS)}

    if use_proxy:
        # if using proxy, enrich the request parameters with a proxy
        while not len(PROXIES) > 0:
            PROXIES = get_valid_proxies_multithreading()

        proxy_ip = random.choice(PROXIES)
        params['proxies'] = {'http': proxy_ip, 'https': proxy_ip}

    return params


def get_request_params_from_urls(urls: List[str], use_header=True, use_proxy=True, timeout=5) -> List[Dict]:

    list_request_params = []
    for url in urls:
        params = get_request_params_from_url(url, use_header=use_header, use_proxy=use_proxy, timeout=timeout)
        list_request_params.append(params)

    return list_request_params


def get_contents_from_urls(
        urls: List[str],
        max_workers: int = 100,
        use_proxy: bool = True,
        timeout: int = None,
        get_timeout: int = 5,
        max_requests_url: int = 5
    ) -> Dict[str, BeautifulSoup]:
    """
        Get content of pages for given URLs
        :param urls: URLs for which we want to extract the content
        :param max_workers: maximum number of threads for execution of requests
        :param use_proxy: use proxies? (default: True)
        :param timeout: timeout in seconds, if execution takes more, return partial results, default: no limit
        :param get_timeout: time out for get requests, default: 5 seconds
        :param max_requests_url: maximum requests to try per url, default: 5
        :return: list of BeautifulSoup objects (one for each url)
        """

    contents = {}
    n_init_urls = len(urls)
    n_requests = 0
    n_iters = 0
    tic = time.time()
    func_name = 'get_contents_from_urls()'
    map_url_reqcount = {url: 0 for url in urls}

    # Send requests in parallel and retry failed requests until the requests for all URLs (pages) are fulfilled.
    while len(urls) > 0:

        # Draw a sample of URLs to try on this iteration, if there are more URLs than max_workers
        urls_sample = random.sample(urls, min(len(urls), max_workers))

        # Get list of parameters to use in get requests
        list_kwargs = get_request_params_from_urls(urls_sample, use_proxy=use_proxy, timeout=get_timeout)

        # Send requests asynchronously and retrieve the results
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(list_kwargs)) as executor:
            results = executor.map(lambda p: send_get_request(**p), list_kwargs)

        for kwargs, result in zip(list_kwargs, results):
            status, content = result['status'], result['content']
            url = kwargs['url']
            if content is not None:
                # if request was successful, keep the result and remove the URL from the list
                contents[url] = content
                urls.remove(url)
            elif status is not None and status != 200:
                # if the request was succesfull, but the site didn't return content for the given URL
                # (e.g. error: 404, 410), then just remove the URL to never try it again
                urls.remove(url)
            else:
                # if request failed, remove the proxy that was used for this request
                if kwargs.get('proxies') is not None:
                    try:
                        proxy_ip = list(kwargs.get('proxies').values())[0]
                        PROXIES.remove(proxy_ip)
                    except ValueError as e:
                        pass  # it was removed already by another thread

            # If URL attempted too many times, remove it, probably the URL is invalid
            map_url_reqcount[url] += 1
            if map_url_reqcount[url] > max_requests_url and url in urls:
                urls.remove(url)

        # If execution time went beyond timeout limit, stop and return partial results
        toc = time.time()
        exec_time_formatted = format_seconds(toc - tic)
        if timeout is not None and (toc - tic) > timeout:
            log.warning(f'{func_name} timed out after {exec_time_formatted}, '
                        f'returning partial results for {len(contents)} URLs out of {n_init_urls}...')
            break

        n_requests += len(urls_sample)
        n_avg_requests_per_url = n_requests / n_init_urls
        n_iters += 1
        log.debug(f'{func_name}: iteration={n_iters}, {len(contents)} URLs extracted out of {n_init_urls} '
                  f'({len(contents)/n_init_urls * 100:.1f}%), {len(PROXIES)} proxies available, '
                  f'{n_avg_requests_per_url:.1f} reqs/url, time elapsed: {exec_time_formatted}')

    return contents


def get_content_from_all_pages(
        search_url: str,
        max_pages: int = config.MAX_PAGES,
        use_proxy: bool = True,
        get_timeout: int = 5,
        max_requests_url: int = 5,
) -> List[BeautifulSoup]:
    """
    Get content of all pages for a given search URL
    :param search_url: search url, e.g. https://www.autoscout24.com/lst/bmw?fregfrom=2000&fregto=2000&pricefrom=500&priceto=2000
    :param max_pages: max pages to crawl, e.g. 20 allowed by site (by design)
    :param use_proxy: use proxies? (default: True)
    :param get_timeout: time out for get requests
    :param max_requests_url: maximum requests to try per url, if limit surpassed return partial results, default: 5
    :return: list of BeautifulSoup objects (one for each page)
    """
    # Compose url for given number of pages into a list of urls
    urls = [f'{search_url}&page={i}' for i in range(1, max_pages + 1)]
    contents = get_contents_from_urls(
        urls=urls,
        use_proxy=use_proxy,
        get_timeout=get_timeout,
        max_requests_url=max_requests_url
    )
    return list(contents.values())


def get_article_ids_from_pages(pages: List[BeautifulSoup], n_articles_max: int = None) -> List[str]:
    """
    Get all articles IDs from a list of pages
    :param pages: list of BeautifulSoup objects
    :param n_articles_max: maximum number of articles to extract
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


def get_all_ids_for_search_url(
        search_url: str,
        n_search_results: int = None,
        cache_location: str = 'local',
    ):

    session = boto3.Session(profile_name=config.AWS_PROFILE_NAME)

    log.debug(f'running get_all_ids_for_search_url(search_url={search_url})')

    if cache_location == 'local':
        # cache dir and json file with ids
        dir_cache = f'{config.DIR_CACHE}/{config.FOLDER_IDS}'
        os.makedirs(dir_cache, exist_ok=True)
        path_file = f'{dir_cache}/{get_hash_from_string(search_url)}.json'

        # load from local cache if available and stop execution
        if os.path.exists(path_file):
            with open(path_file) as f:
                ids = json.load(f)
            log.debug(f'loaded {len(ids)} from local cache')
            return ids
    elif cache_location == 's3':
        # load from s3 ids folder if available and stop execution
        s3 = session.client('s3')
        bucket_name = config.AWS_S3_BUCKET
        key = f'{config.FOLDER_IDS}/{get_hash_from_string(search_url)}.json'

        # Check if the object exists
        try:
            s3.head_object(Bucket=bucket_name, Key=key)
        except:
            log.info(f"JSON file '{key}' does not exist in S3 bucket '{bucket_name}'")
        else:
            s3_object = s3.get_object(Bucket=bucket_name, Key=key)
            ids = json.loads(s3_object['Body'].read().decode('utf-8'))
            return ids

    if n_search_results is None:
        n_search_results = get_numbers_of_articles_from_url(search_url)

    nr_of_pages = calculate_nr_of_pages(nr_results=n_search_results)

    list_bs_pages = get_content_from_all_pages(search_url, max_pages=nr_of_pages)
    ids = get_article_ids_from_pages(list_bs_pages, n_search_results)
    ids = list(set(ids))  # unique IDs

    if cache_location == 'local':
        # save to cache
        with open(path_file, 'w') as f:
            json.dump(ids, f, indent=2)
    elif cache_location == 's3':
        # save to s3 ids folder
        json_data = json.dumps(ids, indent=2)
        try:
            s3.put_object(Bucket=bucket_name, Key=key, Body=json_data,)
        except Exception as e:
            log.error(f'Error putting object to S3: {e}')

    return ids


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
        soup = BeautifulSoup(page.content, 'html.parser')
        json_text = soup.select_one('script[id="__NEXT_DATA__"]').text
    except requests.exceptions.RequestException as e:
        log.debug(f'Failed to get json data for {article_url} with error: {trunc_msg(e)}')

    return json_text, status_code


def get_numbers_of_articles_from_url(url: str, max_trials=7, use_proxy=True, max_trials_via_proxy=5) -> int:
    n_trials = 0

    while n_trials < max_trials:
        params = get_request_params_from_url(url=url, use_proxy=use_proxy)
        result = send_get_request(**params)
        status, content = result['status'], result['content']

        if content is not None:
            # if request was successful, return the number of results for the search url
            json_text = content.select_one('script[id="__NEXT_DATA__"]').text
            obj = json.loads(json_text)
            n_offers = obj['props']['pageProps']['numberOfResults']
            return int(n_offers)
        elif status is not None and status != 200:
            # if the request was succesfull, but the site didn't return content for the given URL
            # (e.g. error: 404, 410), return -1 (error, URL must be incorrect, non-existent)
            return -1
        else:
            # if request failed, remove the proxy that was used for this request
            if params.get('proxies') is not None:
                try:
                    proxy_ip = list(params.get('proxies').values())[0]
                    PROXIES.remove(proxy_ip)
                except ValueError as e:
                    pass

        n_trials += 1

        # if it failed too many times via proxy, then try without proxy
        if use_proxy and n_trials >= max_trials_via_proxy:
            use_proxy = False
            time.sleep(random.randint(1, 3))  # sleep between requests when requests are sent directly, not via proxies

    log.error(f'Failed to extract the number of results for the search url: {url} after {max_trials} attempts.')

    return -1


def calculate_nr_of_pages(
        nr_results: int,
        res_per_page: int = config.MAX_RESULTS_PER_PAGE,
        max_pages: int = config.MAX_PAGES
    ) -> int:
    return min(math.ceil(float(nr_results) / res_per_page), max_pages)


def get_all_article_ids(
        makers: List[str] = None,
        year_range: Tuple[int, int] = None,
        price_range: Tuple[int, int] = None,
        adage: int = None,
        max_results: int = config.MAX_RESULTS,
        max_retrievals: int = None,
        price_step: int = 500,
        cache_location: str = None,
        n_too_many: int = 1_000_000,
):
    """
    Get all car ids and save them to cache folder
    :param max_results: when to stop narrowing the filter, if number of search results is less or equal,
        no further narrowing is performed, default: 400 results (maximum retrievable per search)
    :param max_retrievals: maximum allowed number of IDs retrievals
    """

    # Take variables from 'config'
    if cache_location is None:
        cache_location = config.LOCATION

    if makers is None:
        makers = config.MAKERS

    if year_range is None:
        year_range = config.YEAR_RANGE

    if price_range is None:
        price_range = config.PRICE_RANGE

    if adage is None:
        adage = config.ADAGE



    price_step = math.ceil(price_step / 100) * 100  # make sure is a multiple of 100

    all_ids = []
    retrieved_cache = find_all_json_files_with_ids(cache_location)
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

        pars = stack.pop()
        pars_as_key = json.dumps(pars)
        search_url = compose_search_url(**pars)
        search_url_as_hash = get_hash_from_string(search_url)

        # check if this set of parameters was retrieved before
        n_results = retrieved_counts.get(pars_as_key, None)
        if n_results is not None or search_url_as_hash in retrieved_cache:
            continue  # if it was already retrieved, then skip to not repeat the same work

        # check how many results are found when searching with this set for parameters
        n_results = get_numbers_of_articles_from_url(search_url)
        retrieved_counts[pars_as_key] = n_results  # record the number of results for this set of parameters
        pars_formatted = ' | '.join([f'{k}={v}' for k, v in pars.items()])
        log.info(f'Filter: {pars_formatted}: {n_results} results found.')

        if n_results <= 0:
            # if -1 (error) or 0 (zero results found), then nothing to do, go to next
            continue
        elif n_results <= max_results:
            # if less than maximum results, retrieve all articles IDs, as we don't want to narrow the filter further
            ids = get_all_ids_for_search_url(search_url, n_results, cache_location)
            all_ids.extend(ids)
            n_retrievals += 1
        elif n_results > n_too_many:
            # if too many results, most probably an incorrect url with filters was provided (e.g. non-existent maker)
            # the site returns all articles (~1.8M) for an incorrect search url
            log.warning(f'Found {n_results} results, which is too many to be narrowed with year and price, '
                        f'probably an incorrect URL was requested, will skip this set of parameters: \n {pars_as_key}')
            continue
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
            ids = get_all_ids_for_search_url(search_url, n_results, cache_location)
            all_ids.extend(ids)
            n_retrievals += 1

    return all_ids

# TODO : Change read files with jsons, change get requests by reading whole file and put into list
# TODO : Make more requests at one time with multiple threads
# TODO : Read files local by default or read from s3 bucket


def compose_url_id(id: str, site_url: config.SITE_URL):
    return f'{site_url}/offers/{id}'


def get_content_for_article_ids(
        ids: List[str],
        site_url: str = config.SITE_URL,
        use_proxy: bool = True,
        get_timeout: int = 5,
        max_requests_url: int = 5,
) -> Dict[str, BeautifulSoup]:
    """
    Get content for given IDs
    :param ids: list of IDs to extract
    :param site_url: site url, default: https://www.autoscout24.com
    :param use_proxy: use proxies? (default: True)
    :param get_timeout: time out for get requests
    :param max_requests_url: maximum requests to try per url, if limit surpassed return partial results, default: 5
    :return: list of BeautifulSoup objects (one for each page)
    """

    urls = [compose_url_id(id_, site_url) for id_ in ids]
    dict_url_content = get_contents_from_urls(
        urls=urls,
        use_proxy=use_proxy,
        get_timeout=get_timeout,
        max_requests_url=max_requests_url
    )

    dict_id_content = {}
    for id_ in ids:
        url_key = compose_url_id(id_, site_url)
        content = dict_url_content.get(url_key)
        if content is not None:
            dict_id_content[id_] = content

    return dict_id_content


def get_json_txt_from_article(article_bs: BeautifulSoup) -> str:
    """ Extract json text from the BeautifulSoup object of an article"""
    json_txt = article_bs.select_one('script[id="__NEXT_DATA__"]').text
    json_txt = truncate_useless_data_from_json_text(json_txt)
    return json_txt


def transform_vehicle_equipment(obj: Dict):
    keys = ['comfortAndConvenience', 'entertainmentAndMedia', 'extras', 'safetyAndSecurity']
    for k in keys:
        elems = obj['props']['pageProps']['listingDetails']['vehicle'].get('equipment', {}).get(k, [])
        if len(elems) > 0 and all(isinstance(e, dict) for e in elems):
            obj['props']['pageProps']['listingDetails']['vehicle']['equipment'][k] = [e['id'] for e in elems]
    return obj


def truncate_useless_data_from_json_text(json_txt) -> str:
    # This strips off unused data from json text, decreasing the size of it by ~87%, (~7.5x times smaller)

    # load json text as dictionary object
    obj = json.loads(json_txt)

    # copy the structure of the elements we want to keep
    truncated_obj = copy.deepcopy(config.JSON_TXT_KEEP)

    # override the specified keys with values from obj, truncated size = ~25% of original text size (~4x times smaller)
    update_nested_dict(truncated_obj, obj)

    # override some keys with None, truncated size = ~15% of original text size (~7x times smaller)
    update_nested_dict(truncated_obj, copy.deepcopy(config.JSON_TXT_REMOVE))

    # remove keys with null/none values, this truncates an additional ~2% of text size
    remove_none_from_dict(truncated_obj)

    # transform some elements for smaller size, truncated size = ~13% of original text size (~7.5x times smaller)
    transform_vehicle_equipment(truncated_obj)

    return json.dumps(truncated_obj)


def find_all_json_files_with_ids(location: str = 'local'):

    if location == 'local':
        files_json = glob.glob(f'{config.DIR_CACHE}/{config.FOLDER_IDS}/*.json')
        files_json = [os.path.basename(f).replace('.json', '') for f in files_json]
        return files_json
    elif location == 's3':
        files_json = []
        session = boto3.Session(profile_name=config.AWS_PROFILE_NAME)
        s3 = session.client('s3')
        paginator = s3.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=config.AWS_S3_BUCKET, Prefix=config.FOLDER_IDS)
        try:
            for page in page_iterator:
                for obj in page['Contents']:
                    key = obj.get('Key')
                    file_base_name = key.split('/')[-1]  # e.g. 0a99495b-9bbc-4f0e-acfe-c6930dca8ac7.json
                    files_json.append(file_base_name.replace('.json', ''))
        except Exception as e:
            log.error(f"Error no files with ids: {e}")
        return files_json
    else:
        raise ValueError(f'location={location} not recognized')


def load_all_known_ids_local() -> List[str]:
    files_json = glob.glob(f'{config.DIR_CACHE}/{config.FOLDER_IDS}/*.json')
    all_ids = []

    for file_json in files_json:
        with open(file_json, 'r') as file:
            ids = json.load(file)
            all_ids.extend(ids)

    return all_ids


def load_ids_of_all_extracted_articles_local() -> List[str]:
    files_json = glob.glob(f'{config.DIR_CACHE}/{config.FOLDER_ARTICLES}/*.json')
    all_ids_of_articles = [os.path.basename(f).replace('.json', '') for f in files_json]
    return all_ids_of_articles


def load_all_known_ids_s3():
    session = boto3.Session(profile_name=config.AWS_PROFILE_NAME)
    s3 = session.client('s3')
    # use pagination to extract all keys, not just first 1000
    paginator = s3.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=config.AWS_S3_BUCKET, Prefix=config.FOLDER_IDS)
    all_ids = []
    try:
        for page in page_iterator:
            for obj in page['Contents']:
                key = obj.get('Key')
                response = s3.get_object(Bucket=config.AWS_S3_BUCKET, Key=key)
                ids = json.loads(response['Body'].read().decode('utf-8'))
                all_ids.extend(ids)
    except Exception as e:
        log.error(f'Error getting all known ids from s3, no {e}')

    log.info(f'All Known Ids {len(all_ids)} ')
    return all_ids


def load_ids_of_all_extracted_articles_s3():
    session = boto3.Session(profile_name=config.AWS_PROFILE_NAME)
    s3 = session.client('s3')
    # use pagination to extract all keys, not just first 1000
    paginator = s3.get_paginator('list_objects')
    all_ids_extracted = []
    try:
        for page in paginator.paginate(Bucket=config.AWS_S3_BUCKET, Prefix=config.FOLDER_ARTICLES):
            for obj in page['Contents']:
                key = obj.get('Key')
                file_base_name = key.split('/')[-1]  # e.g. 0a99495b-9bbc-4f0e-acfe-c6930dca8ac7.json
                all_ids_extracted.append(file_base_name.replace('.json', ''))
    except Exception as e:
        log.error(f'Error loading ids of extracted article from s3, no {e}')

    log.info(f'Extracted Ids {len(all_ids_extracted)}')
    return all_ids_extracted


def find_ids_left_to_extract(location: str = None):
    if location is None:
        location = config.LOCATION

    if location == 'local':
        ids_known = load_all_known_ids_local()
        ids_extracted = load_ids_of_all_extracted_articles_local()
    elif location == 's3':
        ids_known = load_all_known_ids_s3()
        ids_extracted = load_ids_of_all_extracted_articles_s3()
    else:
        raise ValueError(f'location={location} not recognized')

    ids_known = set(ids_known)
    ids_extracted = set(ids_extracted)
    ids_left_to_extract = list(ids_known.difference(ids_extracted))
    log.debug(f'found {len(ids_left_to_extract)} IDs left to extract '
              f'({len(ids_known)} known, {len(ids_extracted)} extracted)')

    return ids_left_to_extract


def save_json_txt_to_local(json_txt, id_article):
    dir_local = f'{config.DIR_CACHE}/{config.FOLDER_ARTICLES}'
    os.makedirs(dir_local, exist_ok=True)

    with open(f'{dir_local}/{id_article}.json', 'w') as f:
        f.write(json_txt)


def save_json_txt_to_s3(json_txt, id_article):
    session = boto3.Session(profile_name=config.AWS_PROFILE_NAME)
    s3 = session.client('s3')
    json_data = json.dumps(json_txt)
    key = f'{config.FOLDER_ARTICLES}/{id_article}.json'
    try:
        s3.put_object(Bucket=config.AWS_S3_BUCKET, Key=key, Body=json_data)
    except Exception as e:
        log.error(f'Error putting object to S3: {e}')




def save_json_txt(json_txt, id_article, location: str = 'local'):
    if location == 'local':
        return save_json_txt_to_local(json_txt, id_article)
    elif location == 's3':
        return save_json_txt_to_s3(json_txt, id_article)
    else:
        raise ValueError(f'location={location} not recognized')


def main_extract_json_txt_for_all_known_ids(location: str = None, chunk_size: int = 200):
    log.info('main_extract_json_txt_for_all_known_ids(): Starting...')

    if location is None:
        location = config.LOCATION

    ids = find_ids_left_to_extract(location)
    n_attempted = 0
    n_extracted = 0
    n_init_ids = len(ids)
    pb = tqdm(total=n_init_ids, unit='ID', mininterval=30, miniters=100)

    while len(ids) > 0:
        ids_part, ids = ids[:chunk_size], ids[chunk_size:]
        contents = get_content_for_article_ids(ids_part)
        n_attempted += len(ids_part)

        for id_article, content_article in contents.items():
            try:
                json_txt = get_json_txt_from_article(content_article)
            except:
                log.error(f'Failed to get json txt from BeautifulSoup obj of article with ID: {id_article}')
                continue

            save_json_txt(json_txt=json_txt, id_article=id_article, location=location)
            n_extracted += 1

        log.debug(f'{n_attempted/n_init_ids * 100:.1f}% of IDs attempted, '
                  f'success rate: {n_extracted/n_attempted * 100:.1f}%')
        pb.update(len(ids_part))

    pb.display()
    pb.close()
    log.info('main_extract_json_txt_for_all_known_ids(): Done.')

