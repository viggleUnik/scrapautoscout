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

from scrapautoscout.scrapper import compose_search_url, get_content_from_all_pages, get_article_ids_from_pages, \
    get_hash_from_string, get_numbers_of_offers_from_url, calculate_nr_of_pages
from scrapautoscout import config
from scrapautoscout.proxies import get_valid_proxies_multithreading

log = logging.getLogger(os.path.basename(__file__))


def daily_get_all_ids_for_search_url(search_url: str,
                                     max_pages: int,
                                     last_page_articles: int,
                                     boto_session: boto3.session.Session,
                                     bucket_name: str = config.BUCKET
                                     ):
    # Create json file with car_ids

    # Use the session to create an S3 client
    client = boto_session.client('s3')

    # Create key for file
    hashed_url = get_hash_from_string(search_url)
    t_date = datetime.today().strftime('%Y%m%d')
    key_file_name = f'daily/{t_date}/car_ids/{hashed_url}.json'

    # TODO maybe is needed to check if file exist in s3 bucket

    # Get car_ids to write in a json file
    list_bs = get_content_from_all_pages(search_url, max_pages=max_pages)
    car_ids = get_article_ids_from_pages(list_bs, last_page_articles)
    json_data = json.dumps(car_ids, indent=2)

    # Write file with car_ids to S3 bucket
    client.put_object(
        Bucket=bucket_name,
        Key=key_file_name,
        Body=json_data
    )


def daily_get_all_article_ids_forloop(
        makers: List[str] = config.MAKERS,
        price_ranges: List[List[int]] = config.PRICE_RANGES,
):
    session = boto3.Session(profile_name='default')

    # find results for makers
    for maker in makers:
        # find results for price ranges
        for price_from, price_to in price_ranges:

            search_url = 'https://www.autoscout24.com/lst'
            search_url = compose_search_url(search_url, maker=maker, adage=1, pricefrom=price_from, priceto=price_to)
            log.info(f'SEARCH URL: {search_url}')

            n_results = get_numbers_of_offers_from_url(search_url)
            if n_results is None:
                sleep(300)
                n_results = get_numbers_of_offers_from_url(search_url)

            # Case when no car listed on specified url
            if n_results == 0:
                continue
            elif n_results > 0:
                nr_of_pages, last_page_articles = calculate_nr_of_pages(nr_results=n_results)  # unpacking
                log.info(f'Pages: {nr_of_pages} Found')
                daily_get_all_ids_for_search_url(search_url=search_url, max_pages=nr_of_pages,
                                                 last_page_articles=last_page_articles, boto_session=session)


def daily_read_ids_jsons_files(bucket_name: str = config.BUCKET):
    # TODO function to read from daily/ymd/ids
    # Create a session using the default profile, initialize s3 client
    session = boto3.Session(profile_name='default')
    client = session.client('s3')

    # Prefix
    t_date = datetime.today().strftime('%Y%m%d')
    prefix = f'daily/{t_date}/car_ids/'

    # List all the objects in the bucket with the specified prefix
    objects = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Check if folder exists
    if 'Contents' in objects:
        # Iterate through all the objects in the directory
        for obj in objects['Contents']:
            # Get the object key
            obj_key = obj['Key']
            # Check if the object is a JSON file
            if obj_key.endswith('.json'):
                # Get the object content
                obj_content = client.get_object(Bucket=bucket_name, Key=obj_key)['Body'].read().decode('utf-8')
                # Parse the JSON content
                json_data = json.loads(obj_content)
                # Get articles





# TODO function to write into daily/ymd/articles

def daily_create_articles_folder(
        car_ids: List[str],
        bucket_name: str,
        boto_session: boto3.session.Session
):
    # Use the session to create an S3 client
    client = boto_session.client('s3')
    # Prefix
    t_date = datetime.today().strftime('%Y%m%d')
    prefix = f'daily/{t_date}/articles/'




if __name__ == "__main__":
    daily_read_ids_jsons_files()
