import json
import requests
# insert_into_car_table(obj)
from bs4 import BeautifulSoup
import boto3
import db.insert_data as insert
from datetime import datetime
import os
from db.extract_data import get_details_from_raw_json
from scrapautoscout.proxies import get_valid_proxies_multithreading

aws_access_key_id = os.environ['AWS_SECRET_KEY']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
region_name = 'eu-west-3'

# Creating the low level functional client
client = boto3.client(
    service_name='s3',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key

)
# Creating the high level object oriented interface
resource = boto3.resource(
    service_name='s3',
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# # Code to create a folder into s3 bucket
# bucket_name = 'scrapautoscout-bucket'
# folder_name = 'new-path'
# client.put_object(Bucket=bucket_name, Key=(folder_name+'/'))


# # Code for listing all files and read them
# response = client.list_objects(Bucket='scrapautoscout-bucket')
# for el in response['Contents']:
#     print(el['Key'])
#     obj = client.get_object(Bucket='scrapautoscout-bucket', Key=el['Key'])
#     data = json.load(obj['Body'])
#     print(data)
#     break



# in this response we have listed files within a folder
# response = client.list_objects(Bucket=bucket_name, Prefix=file)

## check if a folder exists
# if 'Contents' not in response:
#
#     # # use boto3 to retrieve keys from a specific folder 'Prefix='
#     # for el in response['Contents']:
#     #     # also check if a file exists
#     #     if el['Key'] == f'{folder_name}{file}':
#     #         print('i found')
#     #     print(el['Key'])
#     print('create folder')
#
# else:
#     # create folder in s3 bucket
#     print('exists')

#####################################
# '''going through all objects in a bucket '''
# count = 0
# mybucket = resource.Bucket(bucket_name)
# for file in mybucket.objects.all():
#
#     if file.size > 2000:
#         json_data = file.get()['Body'].read().decode('utf-8')
#         try:
#             print('first')
#             car_info = get_details_from_raw_json(json_data)
#         except TypeError:
#             print('second')
#             stop = True
#             json_obj = json.loads(json_data)
#         # json_loads = json.loads(json_obj)
#         # print(json_loads['props']['pageProps']['listingDetails'])
#             car_info = get_details_from_raw_json(json_obj)
#         break
# print(car_info)
# insert.insert_into_car_table(car_info)

        # listing_details = json_obj['props']['pageProps']['listingDetails']
        # print(listing_details)


    # obj = resource.Object(bucket_name=bucket_name, key=file.key)
    # response = obj.get()
    # data = response['Body'].read()
    # print(data)
    # if count >= 3:
    #     break
    # count += 1









## Code to read data from a json file from s3 bucket
# obj = client.get_object(
#     Bucket='scrapautoscout-bucket',
#     Key='w3.json'
# )
#
# data = json.load(obj['Body'])
# print(data)


# Check if a folder exists in a bucket or a file in a folder
# zZmk8NI4WBuSga5Ew9jPiQ/ folder in bucket

# bucket='scrapautoscout-bucket'
# folder = 'zZmk8NI4WBuSga5Ew9jPiQ/'
# file_json = 'ffe10e28-0c65-4c28-bbb3-47c56c34d223.json'
# s3 = s3fs.S3FileSystem(anon=False, key=aws_access_key_id, secret=aws_secret_access_key)
# file_path = bucket + '/' + folder + file_json
# folder_path = bucket + '/' + folder
# if s3.exists(file_path):
#     print('File Exists')
# else:
#     print('File doesnt exists')


# # check for directory
# s3.isfile(folder_path)
# # check for file
# s3.isfile(file_path)


# s3.find(path) list all files below path

# for f_s3 in s3.find(folder_path):
#     # s3.open(file_path) Return a file-like object from the filesystem
#     file = s3.open(f_s3, 'rb')
#     json_file = json.load(file)
#     print(json_file)
#     break

# try:
#     client.head_object(Bucket='scrapautoscout-bucket', Key='08tDJafk5GYOiiKCydaNVA/12b2def9-dd6f-4790-abbf-d4c433086aa5.json')
#     print('found')
# except botocore.exceptions.ClientError:
#     print('not found')


# link to cars added 1 day ago
# https://www.autoscout24.com/lst/bmw?adage=1
import time
import os
print(os.cpu_count())
start = time.time()

ip_list = get_valid_proxies_multithreading()

end = time.time()
print(end - start)
print(ip_list)




