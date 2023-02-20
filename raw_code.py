import json
import os
from scrapautoscout.scrapper import get_details_from_raw_json
path = 'cache/get_content_id'

for root, dirs, files in os.walk(path):
    print(root)
    for _dir in dirs:
        print(_dir)
    for _file in files:
        print(_file)
