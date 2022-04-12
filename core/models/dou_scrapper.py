import datetime
import logging
import time
import json
from core.models.edition_builder import EditionBuilder
from core.models.article_chopper import ArticleChopper
from core.models.full_article_scrapper import FullArticleScraper


logging.basicConfig(filename='dou_scrapper.log', filemode='w', format='%(message)s',
                    level=logging.DEBUG)


class DouScrapper:
    def __init__(self, start_date, end_date=None,):
        self._counter = 1
        if end_date:
            self._dates = self._generate_dates(start_date, end_date)
        else:
            self._dates = [start_date]
        self._number_of_dates = len(self._dates)

    def scrape(self):
        print(f'Started scraping {datetime.datetime.now()}')
        while self._dates:
            date = self._dates.pop(0)
            edition = EditionBuilder(date)
            sections = edition.builder()
            chopper = ArticleChopper(sections)
            articles = chopper.chop()
            for article in articles:
                article = FullArticleScraper(article)
                self._save_article(article.return_full_article())
            time.sleep(1)
        print(f'Started scraping {datetime.datetime.now()}')

    def _generate_dates(self, start, end):
        dt = datetime.datetime(self._format_time(start)[0], self._format_time(start)[1], self._format_time(start)[2])
        end = datetime.datetime(self._format_time(end)[0], self._format_time(end)[1], self._format_time(end)[2])
        step = datetime.timedelta(days=1)
        date_list = []
        while dt < end:
            date_list.append(dt.strftime('%d-%m-%Y'))
            dt += step
        return date_list

    @staticmethod
    def _format_time(time_string):
        time_components = time_string.split('-')
        day = int(time_components[0])
        month = int(time_components[1])
        year = int(time_components[2])
        return year, month, day

    @staticmethod
    def _save_article(article):
        with open('output.json', 'a', encoding='utf-8') as file:
            json.dump(article, file, indent=4, ensure_ascii=False)
