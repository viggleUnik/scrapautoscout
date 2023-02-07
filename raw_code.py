import logging

import os

log = logging.getLogger(os.path.basename(__file__))


# valid_ips = []
#
# if not valid_ips:
#     valid_ips = get_valid_proxies_multithreading()
# else:
#     while valid_ips:
#         for ip in valid_ips:
#             try:
#                 response = requests.get('https://www.autoscout24.com/', headers=HEADERS, proxies={'http': ip, 'https': ip},
#                                         timeout=2)
#                 if response.status_code == 200:
#                     print('succes')
#             except:
#                 print('fail')
#                 valid_ips.remove(ip)




