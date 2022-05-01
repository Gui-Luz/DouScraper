import os
from elasticsearch import Elasticsearch, helpers
from core.auxiliary.auxiliary import load_json_from_file, ROOT_PATH


def iterates_over_outuput_dir():
    path = f'{ROOT_PATH}/outputs'
    print(f'[+] Start reading output dir: {path}')
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if len(file) == 69:
                filelist.append((root, file))
    print(f'[+] {len(filelist)} articles found')
    return filelist


def load_articles(files):
    counter = 1
    print(f'[+] Start loading articles articles')
    articles_list = []
    for root, file in files:
        j = load_json_from_file(root + '/', file)
        print(f'[+] {counter} Loading {root}/{file}')
        articles_list.append(j)
        counter += 1
    return articles_list


def bulk_insert(articles):
    client_path = "http://localhost:9200"
    es_client = Elasticsearch(client_path)
    bulk_size = 10000
    number_of_bulks = int(len(articles) / bulk_size) + 1
    print(f'[+] Started connection with ES {client_path}')
    print(f'[+] Will bulk import in chunks of {bulk_size}')
    while articles:
        bulk = []
        for i in range(bulk_size):
            try:
                article = articles.pop(0)
                bulk.append(article)
            except:
                pass
        helpers.bulk(es_client, bulk, index="dou_testev6")
        print(f'[+] {number_of_bulks} bulks to finish...')
        number_of_bulks = number_of_bulks - 1
    print(f'[+] Done!')


if __name__ == '__main__':
    files = iterates_over_outuput_dir()
    articles = load_articles(files)
    bulk_insert(articles)
