import argparse
import os

import scrapautoscout.config as config
# from scrapautoscout import config
from scrapautoscout.scrapper import get_all_article_ids_forloop, read_ids_json_files_from_cache


def run():
    get_all_article_ids_forloop()
    read_ids_json_files_from_cache()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_out', default=config.DIR_CACHE,
                        help='Where to save artifacts. Default: /cache from project root')
    args = parser.parse_args()

    # override default folder for cache
    config.DIR_CACHE = args.dir_out
    os.makedirs(config.DIR_CACHE, exist_ok=True)

    run()
