import argparse
import os

import scrapautoscout.config as config
# from scrapautoscout import config
from scrapautoscout.scrapper import get_all_article_ids_forloop, read_ids_json_files_from_cache


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_out', default=config.DIR_CACHE,
                        help='Where to save artifacts. Default: /cache from project root')
    parser.add_argument('--makers',  nargs='+', type=str, help = 'Parse a list of makers')

    args = parser.parse_args()
    # override default folder for cache
    config.DIR_CACHE = args.dir_out

    os.makedirs(config.DIR_CACHE, exist_ok=True)
    if args.makers is not None:
        get_all_article_ids_forloop(makers=args.makers)
    else:
        get_all_article_ids_forloop()
    read_ids_json_files_from_cache()


if __name__ == "__main__":
    run()
