from scrapautoscout.scrapper import get_all_article_ids_forloop, read_ids_json_files_from_cache


def run():
    get_all_article_ids_forloop()
    read_ids_json_files_from_cache()


if __name__ == "__main__":
    run()
