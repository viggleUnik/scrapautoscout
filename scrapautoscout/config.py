# configs
import logging
import os


class config:
    # Dirs
    # *****************************************************************************
    LOCATION = 'local'  # where is the location to read/write extracted files, 'local' or 's3'?
    FOLDER_CACHE = 'cache'  # name of output folder where to keep extracted articles
    FOLDER_IDS = 'ids'  # folder inside FOLDER_CACHE where to save json files with IDs
    FOLDER_ARTICLES = 'articles'  # folder inside FOLDER_CACHE where to save json files of articles
    FOLDER_ARTIFACTS = 'artifacts'  # folder with artifacts (e.g. logs, etc.)

    # local
    DIR_CACHE = None
    DIR_ARTIFACTS = None

    # aws s3
    AWS_PROFILE_NAME = 'default'
    AWS_S3_BUCKET = 'scrapautoscout-bucket'

    # Logging
    # *****************************************************************************
    LOGS_LEVEL = 'debug'
    FILE_LOGS = None

    # Search
    # *****************************************************************************
    SITE_URL = 'https://www.autoscout24.com'
    MAX_PAGES = 20
    MAX_RESULTS = 400
    MAX_RESULTS_PER_PAGE = 20

    # defaults for search
    ADAGE = 365  # maximum age of ads to extract
    MAKERS = [
        'Audi', 'BMW', 'Ford', 'Mercedes-Benz', 'Opel', 'Renault', 'Volkswagen',
        '9ff', 'Abarth', 'AC', 'ACM', 'Acura', 'Aixam', 'Alfa Romeo', 'Alpina', 'Alpine', 'Amphicar', 'Ariel Motor',
        'Artega', 'Aspid', 'Aston Martin', 'Austin', 'Autobianchi', 'Auverland', 'Baic', 'Bedford', 'Bellier',
        'Bentley', 'Bollore', 'Borgward', 'Brilliance', 'Bugatti', 'Buick', 'BYD', 'Cadillac', 'Caravans-Wohnm',
        'Casalini', 'Caterham', 'Changhe', 'Chatenet', 'Chery', 'Chevrolet', 'Chrysler', 'Citroen', 'CityEL', 'CMC',
        'Corvette', 'Courb', 'Cupra', 'Dacia', 'Daewoo', 'DAF', 'Daihatsu', 'Daimler', 'Dangel', 'De la Chapelle',
        'De Tomaso', 'DFSK', 'Dodge', 'Donkervoort', 'DR Motor', 'DS Automobiles', 'Dutton', 'e.GO',
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

    # What to keep/remove from original json data extracted from the site
    # *****************************************************************************
    JSON_TXT_KEEP = {
        'props': {
            'pageProps': {
                'listingDetails': {
                    'id': None,
                    'description': None,
                    'ratings': None,
                    'prices': {
                        'isFinalPrice': None,
                        'public': None,
                        'dealer': None,
                    },
                    'price': None,
                    'vehicle': None,
                    'location': None,
                    'seller': None,
                    'warranty': None,
                    'warrantyExists': None,
                },
            }
        }
    }

    JSON_TXT_REMOVE = {
        'props': {
            'pageProps': {
                'listingDetails': {
                    'vehicle': {
                        'rawData': {
                            'equipment': None,
                        }
                    },
                    'seller': {
                        'logo': None
                    },
                }
            }
        }
    }

    @staticmethod
    def setup(**kwargs):
        # setup global configs to be used by this application
        # parameters provided via kwargs will override the default configs specified in static attributes of this class
        config.override_defaults(**kwargs)
        config.setup_dirs()
        config.setup_logging()

    @staticmethod
    def override_defaults(**kwargs):
        # overrides the default config values specified in static attributes of this class

        if kwargs.get('LOCATION') is not None:
            config.LOCATION = kwargs.get('LOCATION')

        if kwargs.get('DIR_CACHE') is not None:
            config.DIR_CACHE = kwargs.get('DIR_CACHE')

        if kwargs.get('AWS_PROFILE_NAME') is not None:
            config.AWS_PROFILE_NAME = kwargs.get('AWS_PROFILE_NAME')

        if kwargs.get('AWS_S3_BUCKET') is not None:
            config.AWS_S3_BUCKET = kwargs.get('AWS_S3_BUCKET')

        if kwargs.get('MAKERS') is not None and len(kwargs.get('MAKERS')) > 0:
            config.MAKERS = kwargs.get('MAKERS')

        if kwargs.get('ADAGE') is not None:
            config.ADAGE = kwargs.get('ADAGE')

        if kwargs.get('MAX_RESULTS') is not None:
            config.MAX_RESULTS = kwargs.get('MAX_RESULTS')

        if kwargs.get('LOGS_LEVEL') is not None:
            config.LOGS_LEVEL = kwargs.get('LOGS_LEVEL')

    @staticmethod
    def setup_dirs():
        if config.DIR_ARTIFACTS is None:
            config.DIR_ARTIFACTS = os.path.join(os.getcwd(), config.FOLDER_ARTIFACTS)

        if config.DIR_CACHE is None:
            config.DIR_CACHE = os.path.join(os.getcwd(), config.FOLDER_CACHE)

        os.makedirs(config.DIR_ARTIFACTS, exist_ok=True)
        os.makedirs(config.DIR_CACHE, exist_ok=True)

    @staticmethod
    def setup_logging():
        config.FILE_LOGS = f'{config.DIR_ARTIFACTS}/logs.log'

        # set logging config:
        loglevels_dict = {'debug': logging.DEBUG, 'info': logging.INFO, 'error': logging.ERROR}
        logs_level = loglevels_dict.get(config.LOGS_LEVEL.lower(), logging.INFO)
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(config.FILE_LOGS), logging.StreamHandler()],
            level=logs_level,
        )

        # set all existing loggers to level=LOGS_LEVEL
        loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
        for logger in loggers:
            logger.setLevel(loglevels_dict.get(config.LOGS_LEVEL.lower(), logging.INFO))

        # suppress logs by `urllib3.connectionpool`
        log_urllib3 = logging.getLogger('urllib3.connectionpool')
        log_urllib3.addHandler(logging.NullHandler())
        log_urllib3.propagate = False
        log_urllib3.setLevel(logging.INFO)

        # suppress logs by 'botocore.hooks'
        log_botocore = logging.getLogger('botocore')
        log_botocore.addHandler(logging.NullHandler())
        log_botocore.propagate = False
        log_botocore.setLevel(logging.INFO)
