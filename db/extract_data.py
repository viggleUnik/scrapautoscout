import json
from typing import Dict
import boto3
from scrapautoscout.config import config


def get_details_from_raw_json(json_text: str) -> Dict:
    # TODO: parse the entire json, then return only the content under: object > props > pageProps > listingDetails
    #       return data that can be added to table (name: value)

    item_json = json.loads(json_text)
    listing_details = item_json['props']['pageProps']['listingDetails']

    info = {
        'car_id': listing_details['id'],
        'price': listing_details['prices']['public']['priceRaw'],
        'make': listing_details['vehicle']['make'],
        'model': listing_details['vehicle']['model'],
        'model_version': listing_details['vehicle']['modelVersionInput'],
        'mileage_in_km': listing_details['vehicle']['mileageInKmRaw'],
        'registration_date': listing_details['vehicle']['firstRegistrationDateRaw'],
        'body_type': listing_details['vehicle']['bodyType'],
        'numberOfSeats': listing_details['vehicle']['numberOfSeats'],
        'numberOfDoors': listing_details['vehicle']['numberOfDoors'],
        'body_color': listing_details['vehicle']['bodyColor'],
        'power_in_hp': listing_details['vehicle']['rawPowerInHp'],
        'transmission': listing_details['vehicle']['transmissionType'],
        'gears': listing_details['vehicle']['gears'],
        'rawDisplacementInCCM': listing_details['vehicle']['rawDisplacementInCCM'],
        'fuel_category': listing_details['vehicle']['fuelCategory']['formatted'],
        'city': listing_details['location']['city'],
        'street': listing_details['location']['street'],
        'seller': listing_details['seller']['type']
    }

    return info


def s3_get_data_from_bucket_jsons(bucket_name: str = config.AWS_S3_BUCKET):
    # Create a session using the default profile
    session = boto3.Session(profile_name='default')
    # Use the session to create an S3 client
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(bucket_name)
    for obj in my_bucket.objects.all():
        if obj.size > 2000:
            json_data = obj.get()['Body'].read().decode('utf-8')
            try:
                car_info = get_details_from_raw_json(json_data)
            except TypeError:
                json_obj = json.loads(json_data)
                car_info = get_details_from_raw_json(json_obj)

            # TODO : Insert 'car_info' Into DataBase

