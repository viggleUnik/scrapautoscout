import pandas as pd
import requests  # for making standard html requests
from bs4 import BeautifulSoup  # magical tool for parsing html data
import json
from scrapper import compose_search_url, get_numbers_of_offers_from_url, get_content_from_all_pages, get_article_ids, get_all_ids_for_search_url
from typing import Dict, List, Tuple, Union
def get_ofers_from_years():
    df_offers = pd.DataFrame(columns=['yearfrom', 'yearto'])
    for y in range(1992, 2022, 2):
        row_to_append = pd.DataFrame([{'yearfrom': y, 'yearto': y + 1}])
        df_offers = pd.concat([df_offers, row_to_append])
    top_makers = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'volkswagen', 'renault']
    for make in top_makers:
        offers_per_years = []
        for i in range(1992, 2022, 2):
            url = 'https://www.autoscout24.com/lst/'
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            offers_url = f'{url}{make}?fregfrom={i}&fregto={i + 1}'
            page = requests.get(offers_url, headers=HEADERS)
            soup = BeautifulSoup(page.text, 'html.parser')
            item = soup.select_one('script[id="__NEXT_DATA__"]').text
            json_file = json.loads(item)
            offers = json_file['props']['pageProps']['numberOfResults']
            offers_per_years.append(offers)



    df_offers[make] = offers_per_years

    return df_offers

from time import sleep
from random import randint


max_results = 400
top_makers = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'volkswagen', 'renault']
search_url = 'https://www.autoscout24.com/lst'
price_ranges = [
    [2_000, 5_000],
    [5_001, 10_000],
    [10_001, 13_000],
    [13_001, 16_000],
    [16_001, 20_000],
    [20_001, 25_000],
    [25_001, 30_000],
    [30_001, 35_000],
    [35_001, 40_000],
    [40_001, 50_000],
    [50_001, 60_000],
    [60_001, 80_000],
    [80_001, 100_000],
    [100_001, 9_999_999],
]
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


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
            print(search_url)
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


get_all_article_ids_forloop(search_url='https://www.autoscout24.com/lst',
                            max_results=400,
                            makers=['renault'],
                            years=list(range(1992, 2023)),
                            price_ranges=price_ranges
                            )


# nr_offers = get_numbers_of_offers_from_url(
#     'https://www.autoscout24.com/lst/bmw?fregfrom=1992&fregto=1992')
# print(f'nr offers {nr_offers}')
# nr_pages_articles = calculate_nr_of_pages(nr_offers)
# print(f'pages articles {nr_pages_articles}')
#
# article_ids = get_all_ids_for_search_url(
#     'https://www.autoscout24.com/lst/bmw?fregfrom=1992&fregto=1992',
#     nr_pages_articles[0], nr_pages_articles[1])
# print(article_ids)
# print(f'lenght {len(article_ids)}')

# with open(
#     'cache/aHR0cHM6Ly93d3cuYXV0b3Njb3V0MjQuY29tL2xzdC9hdWRpP2ZyZWdmcm9tPTIwMDEmZnJlZ3RvPTIwMDEmcHJpY2Vmcm9tPTEzMDAxJnByaWNldG89MTYwMDA.json',
#     'r') as file:
#     json_object = json.load(file)
#
# for id in json_object:
#     print(id)

