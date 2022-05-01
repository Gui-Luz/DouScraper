from datetime import datetime
import os
import json
import requests
from bs4 import BeautifulSoup as bs


HEADER = {

    "Host": "www.in.gov.br",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": "COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=pt_BR; _ga=GA1.3.945755959.1647545759; "
              "_gid=GA1.3.225074147.1647975513; LFR_SESSION_STATE_20158=1647977035212; "
              "JSESSIONID=YPv1AI6jbuzIlcQUbkuLhdSjC1ex8h4dzIbn9Y08.sinvp-215; _gat=1",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Cache-Control": "max-age=0",
}

ROOT_PATH = os.getcwd().split('/core')[0]


def request_url(url):
    r = requests.get(url, headers=HEADER)
    return r.text


def get_soup(html):
    soup = bs(html, 'html.parser')
    return soup


def get_section(url):
    try:
        html = request_url(url)
        soup = get_soup(html)
        script = soup.find("script", id="params")
        j = json.loads(script.text)
        return j, None
    except Exception as e:
        print(e)
        return None, e


def format_date_for_elk(date_string):
    date_object = datetime.strptime(date_string, "%d/%m/%Y")
    return str(date_object.date())


def format_date(date_string):
    date_object = datetime.strptime(date_string, "%d-%m-%Y")
    date_string = date_object.strftime('%Y-%m-%d')
    return date_string


def log_error(error):
    with open('./outputs/error_log.txt', 'a') as file:
        file.write(error)


def load_json_from_file(path, file):
    with open(path + file, 'r') as file:
        j = json.load(file)
    return j


def get_files_in_dir(path):
    files = os.listdir(path)
    return files

