import os.path
import requests  # for making standard html requests
from bs4 import BeautifulSoup  # magical tool for parsing html data
import json  # for parsing data
from time import sleep
from typing import Dict, List, Tuple
import logging
import base64
import hashlib
import random

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

    if not search_url.endswith('/lst'):
        search_url = f'{search_url}/lst'

    if maker is not None:
        search_url = f'{search_url}/{maker.lower()}?'

    if not search_url.endswith('?'):
        search_url = f'{search_url}?'

    filters = {
        'fregfrom': fregfrom,
        'fregto': fregto,
        'pricefrom': pricefrom,
        'priceto': priceto,
        'adage': adage,
    }

    filters.update(kwargs)

    # filter fields which are not None
    filters = {k: v for k, v in filters.items() if v is not None}
    filters_str_pairs = [f'{k}={v}' for k, v in filters.items()]
    filters_compounded = '&'.join(filters_str_pairs)
    search_url = f'{search_url}{filters_compounded}'


    # examples returned
    # https://www.autoscout24.com/lst/bmw?fregfrom=2020&fregto=2020&pricefrom=20000&priceto=23000&page=2
    # https://www.autoscout24.com/lst/bmw?fregfrom=2000&fregto=2000&pricefrom=500&priceto=2000

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
    :param max_pages: 20 allowed
    :return: list of BS
    """
    if headers is None:
        headers = {'User-Agent': random.choice(config.USER_AGENTS)}

    pages = []
    # get valid proxies for rotation
    proxies_valid_ips = get_valid_proxies_multithreading()

    for i in range(1, max_pages + 1):
        found = False
        while not found:
            if len(proxies_valid_ips) == 0:
                proxies_valid_ips = get_valid_proxies_multithreading()

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

    return pages


def get_article_ids(pages: List[BeautifulSoup], nr_articles_last: int = None) -> List[str]:
    """
    Get all articles IDs in a list of pages
    :param pages: list of BS
    :return: list of article IDs
    """
    # case when we have full pages, 20 articles per page
    article_ids = []
    if nr_articles_last == 0:
        for page in pages:
            # Find all articles id on a page
            articles_per_page = page.find_all('article')
            for article in articles_per_page:
                article_ids.append(article.get('id'))

    # case when we have 1 incomplete page
    elif len(pages) == 1:
        last_page_articles = pages[0].find_all('article')
        for count, article in enumerate(last_page_articles):
            if count >= nr_articles_last:
                break
            article_ids.append(article.get('id'))

    # case when we have pages with one last page incomplete
    elif len(pages) > 1:
        for page in pages[:-1]:
            articles_per_page = page.find_all('article')
            for article in articles_per_page:
                article_ids.append(article.get('id'))

        last_page_articles = pages[-1].find_all('article')

        for count, article in enumerate(last_page_articles):
            if count >= nr_articles_last:
                break
            article_ids.append(article.get('id'))

    return article_ids


def get_hash_from_string(s: str) -> str:
    md5bytes = hashlib.md5(s.encode()).digest()
    hash_str = base64.urlsafe_b64encode(md5bytes).decode('ascii')
    hash_str = ''.join(c for c in hash_str if c.isalnum())
    return hash_str


def get_all_ids_for_search_url(search_url: str, max_pages: int, last_page_articles: int):
    name_file = get_hash_from_string(search_url) + '.json'

    dir_cache = f'{config.DIR_CACHE}/get_all_ids_for_search_url'
    os.makedirs(dir_cache, exist_ok=True)
    path_file = f'{dir_cache}/{name_file}'

    if os.path.exists(path_file):
        with open(path_file) as f:
            ids = json.load(f)
    else:
        list_bs = get_content_from_all_pages(search_url, max_pages=max_pages)
        ids = get_article_ids(list_bs, last_page_articles)
        with open(path_file, 'w') as f:
            json.dump(ids, f, indent=2)

    return ids


def get_json_data_from_article(
        article_id: str,
        site_url: str = config.SITE_URL,
        headers: Dict=None,
        proxy: Dict=None,
) -> str:

    if headers is None:
        headers = config.HEADERS

    article_url = f'{site_url}/offers/{article_id}'
    json_text = None
    try:
        page = requests.get(article_url, headers=headers, proxies=proxy, timeout=5)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'html.parser')
        json_text = soup.select_one('script[id="__NEXT_DATA__"]').text
    except requests.exceptions.RequestException as e:
        log.debug(f'error {e}')
        pass

    return json_text


def get_details_from_raw_json(json_text: str) -> Dict:
    # TODO: parse the entire json, then return only the content under: object > props > pageProps > listingDetails
    #       return data that can be added to table (name: value)

    item_json = json.loads(json_text)
    listing_details = item_json['props']['pageProps']['listingDetails']

    info = {
        'price': listing_details['prices']['public']['priceRaw'],
        'make': listing_details['vehicle']['make'],
        'model': listing_details['vehicle']['model'],
        'model_version': listing_details['vehicle']['modelVersionInput'],
        'mileage_in_km': listing_details['vehicle']['mileageInKmRaw'],
        'registration_date': listing_details['vehicle']['firstRegistrationDateRaw'],
        'body_type': listing_details['vehicle']['bodyType'],
        'body_color': listing_details['vehicle']['bodyColor'],
        'power_in_hp': listing_details['vehicle']['rawPowerInHp'],
        'transmission': listing_details['vehicle']['transmissionType'],
        'gears': listing_details['vehicle']['gears'],
        'fuel_category': listing_details['vehicle']['fuelCategory']['formatted'],
        'location': {
            'city': listing_details['location']['city'],
            'street': listing_details['location']['street'],
        },
        'sealer': listing_details['seller']['type']
    }

    return info


def get_numbers_of_offers_from_url(url: str) -> int:
    page = requests.get(url, headers=config.HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')
    json_text = soup.select_one('script[id="__NEXT_DATA__"]').text
    obj = json.loads(json_text)
    n_offers = obj['props']['pageProps']['numberOfResults']
    sleep(random.randint(0, 3))
    return int(n_offers)


def calculate_nr_of_pages(nr_results: int) -> Tuple[int, int]:
    nr_of_pages = nr_results // 20
    last_page_articles = nr_results % 20

    if nr_of_pages > 20:
        pages_last_articles = (20, 0)
        return pages_last_articles
    elif last_page_articles > 0:
        nr_of_pages += 1

    return nr_of_pages, last_page_articles


def get_all_article_ids_forloop(
        max_results: int = config.MAX_RESULTS,
        makers: List[str] = config.MAKERS,
        years: List[int] = config.YEARS,
        price_ranges: List[List[int]] = config.PRICE_RANGES,
):
    """Get All car ids cached in folder 'get_all_ids_for_search_url' """

    # find results for makers
    for maker in makers:
        # find results for years of registration
        for year in years:
            search_url = 'https://www.autoscout24.com/lst'
            search_url = compose_search_url(search_url, maker=maker, fregfrom=year, fregto=year)
            n_results = get_numbers_of_offers_from_url(search_url)

            if n_results == 0:
                continue
            elif n_results < max_results:
                nr_of_pages, last_page_articles = calculate_nr_of_pages(nr_results=n_results)  # unpacking
                log.debug(f'NR OF PAGES {nr_of_pages} and LAST PAGE ARTICLES {last_page_articles}')
                ids = get_all_ids_for_search_url(search_url, nr_of_pages, last_page_articles)

            elif n_results > max_results:

                for price_from, price_to in price_ranges:
                    search_url = 'https://www.autoscout24.com/lst'
                    search_url = compose_search_url(search_url, maker=maker, fregfrom=year, fregto=year,
                                                    pricefrom=price_from, priceto=price_to)
                    n_results = get_numbers_of_offers_from_url(search_url)

                    if n_results == 0:
                        continue
                    elif n_results > 0:
                        nr_of_pages, last_page_articles = calculate_nr_of_pages(nr_results=n_results)
                        log.debug(f'NR OF PAGES {nr_of_pages} and LAST PAGE ARTICLES {last_page_articles}')
                        ids = get_all_ids_for_search_url(search_url, nr_of_pages, last_page_articles)


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
                if len(proxies_valid_ips) == 0:
                    proxies_valid_ips = get_valid_proxies_multithreading()

                # choose randon proxy from list
                proxy_ip = random.choice(proxies_valid_ips)
                proxy = {'http': proxy_ip, 'https': proxy_ip}
                print(f'proxy {proxy}')

                # choose random user agent from stored USER_AGENTS
                user_agent = random.choice(config.USER_AGENTS)
                json_text = get_json_data_from_article(
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
                            json.dump({}, f, indent=2)
                        request_try = 0

                    elif request_try < 3:
                        request_try += 1
                        proxies_valid_ips.remove(proxy_ip)


