# configs
import logging
import os

# Dirs
# *****************************************************************************
# local
DIR_ARTIFACTS = os.path.join(os.getcwd(), 'artifacts')
os.makedirs(DIR_ARTIFACTS, exist_ok=True)
DIR_CACHE = os.path.join(os.getcwd(), 'cache')
os.makedirs(DIR_CACHE, exist_ok=True)
# aws s3
AWS_S3_BUCKET = 'scrapautoscout-bucket'

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

# suppress logs by `urllib3.connectionpool`
log_urllib3 = logging.getLogger('urllib3.connectionpool')
log_urllib3.addHandler(logging.NullHandler())
log_urllib3.propagate = False
log_urllib3.setLevel(logging.INFO)

# Search
# *****************************************************************************
SITE_URL = 'https://www.autoscout24.com'
MAX_PAGES = 20
MAX_RESULTS = 400
MAX_RESULTS_PER_PAGE = 20

ADAGE = 365  # maximum age of ads to extract
# MAKERS = ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'volkswagen', 'renault']
MAKERS = [
    'Audi', 'BMW', 'Ford', 'Mercedes-Benz', 'Opel', 'Renault', 'Volkswagen',
    '9ff', 'Abarth', 'AC', 'ACM', 'Acura', 'Aixam', 'Alfa Romeo', 'Alpina', 'Alpine', 'Amphicar', 'Ariel Motor',
    'Artega', 'Aspid', 'Aston Martin', 'Austin', 'Autobianchi', 'Auverland', 'Baic', 'Bedford', 'Bellier',
    'Bentley', 'Bollore', 'Borgward', 'Brilliance', 'Bugatti', 'Buick', 'BYD', 'Cadillac', 'Caravans-Wohnm',
    'Casalini', 'Caterham', 'Changhe', 'Chatenet', 'Chery', 'Chevrolet', 'Chrysler', 'Citroen', 'CityEL', 'CMC',
    'Corvette', 'Courb', 'Cupra', 'Dacia', 'Daewoo', 'DAF', 'Daihatsu', 'Daimler', 'Dangel', 'De la Chapelle',
    'De Tomaso', 'Derways', 'DFSK', 'Dodge', 'Donkervoort', 'DR Motor', 'DS Automobiles', 'Dutton', 'e.GO',
    'Estrima', 'Ferrari', 'Fiat', 'FISKER', 'Gac Gonow', 'Galloper', 'GAZ', 'Geely', 'GEM', 'GEMBALLA',
    'Genesis', 'Gillet', 'Giotti Victoria', 'GMC', 'Great Wall', 'Grecav', 'Haima', 'Hamann', 'Honda', 'HUMMER',
    'Hurtan', 'Hyundai', 'Infiniti', 'Innocenti', 'Iso Rivolta', 'Isuzu', 'Iveco', 'IZH', 'Jaguar', 'Jeep',
    'Karabag', 'Kia', 'Koenigsegg', 'KTM', 'Lada', 'Lamborghini', 'Lancia', 'Land Rover', 'LDV', 'Lexus',
    'Lifan', 'Ligier', 'Lincoln', 'Lotus', 'Mahindra', 'MAN', 'Mansory', 'Martin Motors', 'Maserati', 'Maxus',
    'Maybach', 'Mazda', 'McLaren', 'Melex', 'MG', 'Microcar', 'Minauto', 'MINI', 'Mitsubishi', 'Mitsuoka',
    'Morgan', 'Moskvich', 'MP Lafer', 'MPM Motors', 'Nio', 'Nissan', 'Oldsmobile', 'Oldtimer', 'Pagani',
    'Panther Westwinds', 'Peugeot', 'PGO', 'Piaggio', 'Plymouth', 'Pontiac', 'Porsche', 'Proton', 'Puch',
    'Qoros', 'Qvale', 'RAM', 'Reliant', 'Rolls-Royce', 'Rover', 'Ruf', 'Saab', 'Santana', 'Savel', 'SDG',
    'SEAT', 'Shuanghuan', 'Skoda', 'smart', 'SpeedArt', 'Spyker', 'SsangYong', 'StreetScooter', 'Subaru',
    'Suzuki', 'TagAZ', 'Talbot', 'Tasso', 'Tata', 'Tazzari EV', 'TECHART', 'Tesla', 'Town Life', 'Toyota',
    'Trabant', 'Triumph', 'Trucks-Lkw', 'TVR', 'UAZ', 'VAZ', 'VEM', 'Volvo', 'Vortex', 'Wallys', 'Wartburg',
    'Westfield', 'Wiesmann', 'Zastava', 'ZAZ', 'Zhidou', 'Zotye', 'Others'
]
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
YEAR_RANGE = (1980, 2023)
PRICE_RANGE = (500, 1_000_000)

# Enhance requests (to avoid being banned)
# *****************************************************************************
# copied from https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5351.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50",
    "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0",
    "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
]
