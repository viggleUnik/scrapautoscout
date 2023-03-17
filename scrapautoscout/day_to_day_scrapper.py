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
import boto3
from datetime import datetime

from scrapautoscout.scrapper import compose_search_url, get_content_from_all_pages, get_article_ids, \
    get_hash_from_string, get_numbers_of_offers_from_url, calculate_nr_of_pages
from scrapautoscout import config
from scrapautoscout.proxies import get_valid_proxies_multithreading

log = logging.getLogger(os.path.basename(__file__))


def s3_1day_get_all_ids_for_search_url(
        search_url: str,
        boto_session: boto3.session.Session,
        bucket_name: str = config.AWS_S3_BUCKET,
        n_search_results: int = None,
    ):
    # Create json file with ids

    # Use the session to create an S3 client
    client = boto_session.client('s3')

    # Create key for file
    hashed_url = get_hash_from_string(search_url)
    t_date = datetime.today().strftime('%Y-%m-%d')
    key_file_name = f'day-to-day/ids/{t_date}/{hashed_url}-{t_date}.json'

    # TODO maybe is needed to check if file exist in s3 bucket

    if n_search_results is None:
        n_search_results = get_numbers_of_offers_from_url(search_url)

    nr_of_pages = calculate_nr_of_pages(nr_results=n_search_results)

    # Get ids to write in a json file
    list_bs = get_content_from_all_pages(search_url, max_pages=nr_of_pages)
    ids = get_article_ids(list_bs, n_search_results)

    # Write file with ids to S3 bucket
    client.put_object(
        Bucket=bucket_name,
        Key=key_file_name,
        Body=ids
    )


def s3_1day_get_all_article_ids_forloop(
        makers: List[str] = config.MAKERS,
        price_ranges: List[List[int]] = config.PRICE_RANGES,
):
    session = boto3.Session(profile_name='default')

    # find results for makers
    for maker in makers:
        # find results for price ranges
        for price_from, price_to in price_ranges:
            search_url = compose_search_url(smaker=maker, adage=1, pricefrom=price_from, priceto=price_to)
            n_results = get_numbers_of_offers_from_url(search_url)

            if n_results == -1:
                # case when failed
                continue
            elif n_results == 0:
                # Case when no car listed on specified url
                continue
            elif n_results > 0:
                s3_1day_get_all_ids_for_search_url(
                    search_url=search_url,
                    boto_session=session,
                    n_search_results=n_results
                )
