import os
import random
import logging

import config
from scrapautoscout.scrapper import get_all_article_ids, find_ids_left_to_extract, extract_json_txt_for_known_ids


log = logging.getLogger(os.path.basename(__file__))


def run():
    """
    Full pipeline to extract articles, which includes:
      - find all article IDs
      - find which IDs are left to be extracted
      - extract json txt to files
    Execution speed: 14975 IDs in 28min (~9IDs/sec, 2.5days for 2M IDs)
    """

    makers = random.sample(config.MAKERS, len(config.MAKERS))
    # makers = ['Porsche']

    for i, maker in enumerate(makers):
        log.debug(f'maker={maker} ({i} of {len(makers)})')

        log.debug(f'start get_all_article_ids() ...')
        get_all_article_ids(makers=[maker])

        log.debug(f'find_ids_left_to_extract() ...')
        find_ids_left_to_extract(location='local')

        log.debug(f'extract_json_txt_for_known_ids() ...')
        extract_json_txt_for_known_ids(location='local', chunk_size=100)


if __name__ == '__main__':
    run()
