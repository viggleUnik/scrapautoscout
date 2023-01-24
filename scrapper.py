import os.path

import requests  # for making standard html requests
from bs4 import BeautifulSoup  # magical tool for parsing html data
import json  # for parsing data
from time import sleep
from random import randint
from typing import Dict, List, Tuple
import logging
import base64


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


SITE_URL = 'https://www.autoscout24.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
MAX_PAGES = 20
MAX_RESULTS = 400
MAKERS = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'volkswagen', 'renault']
YEARS = list(range(1992, 2023))
PRICE_RANGES = [
    [2_000, 5_000],
    [5_001, 10_000],
    [10_001, 20_000],
    [20_001, 30_000],
    [30_001, 40_000],
    [40_001, 50_000],
    [50_001, 60_000],
    [60_001, 80_000],
    [80_001, 100_000],
    [100_001, 9_999_999],
]


def compose_search_url(
        search_url: str = SITE_URL,
        maker: str = None,
        fregfrom: int = None,
        fregto: int = None,
        pricefrom: int = None,
        priceto: int = None,
        adage: int = None,
        **kwargs,
) -> str:

    if '/lst' not in search_url:
        search_url = f'{search_url}/lst'

    if maker is not None:
        search_url = f'{search_url}/{maker.lower()}?'

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
        max_pages: int = MAX_PAGES,
        max_sleep: int = 5,
) -> List[BeautifulSoup]:
    """
    Get content of all pages for a given search
    :param search_url: search url, e.g. https://www.autoscout24.com/lst/bmw?fregfrom=2000&fregto=2000&pricefrom=500&priceto=2000
    :param headers: headers
    :param max_pages: 20 allowed
    :return: list of BS
    """

    if headers is None:
        headers = HEADERS

    pages = []

    for i in range(1, max_pages+1):
        url_page = f'{search_url}&page={i}'
        page = requests.get(url_page, headers=headers)
        sleep(randint(0, max_sleep))
        soup = BeautifulSoup(page.text, 'html.parser')
        pages.append(soup)

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


def get_all_ids_for_search_url(search_url: str, max_pages: int, last_page_articles: int):
    name_file = base64.b64encode(search_url.encode()).decode()
    name_file = ''.join(c for c in name_file if c.isalnum())
    name_file = name_file + '.json'

    dir_cache = f'cache/get_all_ids_for_search_url'
    os.makedirs(dir_cache, exist_ok=True)
    path_file = f'{dir_cache}/{name_file}'

    if os.path.exists(path_file):
        with open(path_file) as f:
            ids = json.load(f)
    else:
        list_bs = get_content_from_all_pages(search_url, max_pages=max_pages)
        ids = get_article_ids(list_bs, last_page_articles)
        with open(path_file, 'w') as f:
            json.dump(ids, f)

    return ids


def get_json_data_from_article(
        article_id: str,
        site_url: str = SITE_URL,
        headers: Dict=None,
) -> str:

    if headers is None:
        headers = HEADERS

    article_url = f'{site_url}/offers/{article_id}'
    page = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    json_text = soup.select_one('script[id="__NEXT_DATA__"]').text

    return json_text


def get_details_from_raw_json(json_text: str) -> Dict:
    # TODO: parse the entire json, then return only the content under: object > props > pageProps > listingDetails
    #       return data that can be added to table (name: value)
    # {'offer_details': {price: , ...},
    # 'vehicle_details': {'maker': ...}}

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
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')
    json_text = soup.select_one('script[id="__NEXT_DATA__"]').text
    obj = json.loads(json_text)
    n_offers = obj['props']['pageProps']['numberOfResults']
    sleep(randint(0, 3))
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
        max_results: int = None,
        makers: List[str] = None,
        years: List[int] = None,
        price_ranges: List[List[int]] = None
):

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
                        ids = get_all_ids_for_search_url(search_url, nr_of_pages, last_page_articles)

