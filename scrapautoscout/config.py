# configs
import logging
import os
from pathlib import Path

# Dirs
# *****************************************************************************
DIR_ARTIFACTS = os.path.join(os.getcwd(), 'artifacts')
os.makedirs(DIR_ARTIFACTS, exist_ok=True)
DIR_CACHE = os.path.join(os.getcwd(), 'cache')
os.makedirs(DIR_CACHE, exist_ok=True)

# Logging
# *****************************************************************************
LOGS_LEVEL = logging.DEBUG
FILE_LOGS = f'{DIR_ARTIFACTS}/logs.log'
# set logging config:
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(FILE_LOGS), logging.StreamHandler()],
    level=LOGS_LEVEL,
)


#
SITE_URL = 'https://www.autoscout24.com'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}

USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 7.0; d-01J Build/HUAWEIBTV-L0J; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 11; pt-pt; moto g(10) Build/RRB31.Q1-3-69) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36 PHX/11.9',
    'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.147 Mobile Safari/537.36 XiaoMi/MiuiBrowser/14.5.14',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3_5; rv:118.0) Gecko/20110101 Firefox/118.0',
    'Mozilla/5.0 (Linux; arm_64; Android 12; M2103K19Y) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.7.43.00 SA/3 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; A101LV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.215 Safari/537.36 OPR/73.2.3844.69974',
    'Mozilla/5.0 (Linux; U; Android 13; zh-cn; 22041211AC Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.102 MQQBrowser/13.5 Mobile Safari/537.36 COVC/046333',
    'Mozilla/5.0 (Linux; Android 11; Mi Pad5 Pro Wi-Fi) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Mobile Safari/537.36 EdgA/86.0.622.68',
    'Mozilla/5.0 (Linux; U; Android 12; de-de; POCO M4 5G Build/SP1A.210812.016) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.116 Mobile Safari/537.36 XiaoMi/MiuiBrowser/12.22.0.3-gn',
    'Mozilla/5.0 (Linux; Android 12; V2055A; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 VivoBrowser/12.7.0.1',
    'Mozilla/5.0 (Linux; Android 12; LSA-AN00 Build/HONORLSA-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.105 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 Safari/605.1.15 Sleipnir/4.5.2m',
    'Mozilla/5.0 (Linux; Android 4.4.2; Archos 70b Copper Build/Archos; ru-ru) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 Puffin/8.4.0.42087AT',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) Gecko/20100101 Firefox/59.4',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1652.0',
    'Mozilla/5.0 (Linux; Android 9; V1930A Build/PKQ1.190616.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 VivoBrowser/10.1.22.1',
    'Mozilla/5.0 (Android 10; Mobile; rv:105.0; Ghostery:3.0) Gecko/105.0 Firefox/105.0',
    'Mozilla/5.0 (Linux; Android 10; V1829T; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 VivoBrowser/13.5.2.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.9) Gecko/20100101 Goanna/3.2 Firefox/45.9 PaleMoon/27.4.1',
    'Mozilla/5.0 (Linux; Android 10; HarmonyOS; BRQ-AN00; HMSCore 6.9.0.302) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 HuaweiBrowser/13.0.3.301 Mobile Safari/537.36'
]

MAX_PAGES = 20
MAX_RESULTS = 400
MAKERS = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'volkswagen', 'renault']
YEARS = list(range(1992, 2023))
PRICE_RANGES = [
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
