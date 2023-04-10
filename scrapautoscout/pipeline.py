import os
import logging
import argparse
import json

from scrapautoscout.config import config
from scrapautoscout.scrapper import get_all_article_ids, find_ids_left_to_extract, \
    main_extract_json_txt_for_all_known_ids


def run():
    """
    Full pipeline to extract articles, which includes:
      - find all article IDs
      - find which IDs are left to be extracted
      - extract json txt to files
    Execution speed: ~9 IDs/sec, ETA: 2.5days for 2M IDs (based on a run of 14,975 IDs done in 28min)
    Disk space: 0.01Mb/article, est: 20.6 Gb for 2M IDs (481.4 MB on disk for 46,581 items)

    # example of how to run locally:
    # python3 -m scrapautoscout.pipeline

    # example of how to run on AWS EC2 in background, without writing to nohup.out:
    # nohup python3 -m scrapautoscout.pipeline >/dev/null 2>&1
    """

    parser = argparse.ArgumentParser(
        prog='Scrapper autoscout24',
        description='Full pipeline to extract articles from autoscout24'
    )
    parser.add_argument('--LOCATION', help="'local' or 's3'")
    parser.add_argument('--DIR_CACHE', help="Where to save artifacts. Default: 'cache' (relative to project root)")
    parser.add_argument('--AWS_PROFILE_NAME', help='AWS profile name')
    parser.add_argument('--AWS_S3_BUCKET', help='AWS S3 bucket')
    parser.add_argument('--MAKERS', nargs='+', help='List of makers delimited by space')
    parser.add_argument('--LOGS_LEVEL', help="Log level, e.g. 'debug', 'info', 'error'")
    args = parser.parse_args()

    config.setup(**vars(args))

    log = logging.getLogger(os.path.basename(__file__))
    log.info(f'Running {os.path.basename(__file__)}, with parameters: \n' + json.dumps(vars(args), indent=2))

    for i, maker in enumerate(config.MAKERS):
        log.info(f'Extract maker={maker} ({i+1} of {len(config.MAKERS)})...')

        log.info('Get all article IDs...')
        get_all_article_ids(makers=[maker])

        log.info('Find article IDs left to extract...')
        find_ids_left_to_extract()

        log.info('Extract json data of articles...')
        main_extract_json_txt_for_all_known_ids()


if __name__ == '__main__':
    run()
