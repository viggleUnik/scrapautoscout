import json
from typing import Dict
import boto3
from scrapautoscout.config import config
from scrapautoscout.transform import get_details_from_raw_json
from db.insert_data import insert_into_car_table
import datetime


def s3_get_data_insert_db_current_day(bucket_name: str = config.AWS_S3_BUCKET,  ):
    # Create a session using the default profile
    session = boto3.Session(profile_name='default')
    # Use the session to create an S3 client
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    # folder '/articles'
    folder_prefix = 'articles/'

    # get current day
    current_datetime = datetime.datetime.now()
    current_date = current_datetime.date()

    # for obj in my_bucket.objects.all():
    for obj in my_bucket.objects.filter(Prefix=folder_prefix):

            json_data = obj.get()['Body'].read().decode('utf-8')
            last_modified_date = obj.last_modified.date()
            if current_date == last_modified_date:
                try:
                    car_info = get_details_from_raw_json(json_data)
                except TypeError:
                    json_obj = json.loads(json_data)
                    car_info = get_details_from_raw_json(json_obj)

                # insert data into database
                insert_into_car_table(car_info)