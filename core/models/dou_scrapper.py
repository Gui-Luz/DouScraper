import datetime
from core.models.edition import Edition
from core.models.sections import Sections
from core.models.articles import Articles, FullArticles


class DouScrapper:
    def __init__(self, start_date, end_date=None):
        if end_date:
            self._dates = self._generate_dates(start_date, end_date)
        else:
            self._dates = [start_date]
        self._number_of_dates = len(self._dates)
        self._editions = []
        self._sections = []
        self._full_articles = []

    def scrape(self):
        print(f'[+][+][+][+] Started scraping at {datetime.datetime.now()}')
        print(f'[+][+][+][+] Will scrape {len(self._dates)} DOU editions.')
        while self._dates:
            date = self._dates.pop(0)
            edition = Edition(date)
            if edition.exists:
                sections = Sections(edition)
                articles = Articles(sections.sections)
                full_articles = FullArticles(articles.articles)
                self._editions.append(edition)
                self._sections.append(sections)
                self._full_articles.append(full_articles)
        print(f'[+][+][+][+] Stoped scraping at {datetime.datetime.now()}')

    def _generate_dates(self, start, end):
        dt = datetime.datetime(self._format_time(start)[0], self._format_time(start)[1], self._format_time(start)[2])
        end = datetime.datetime(self._format_time(end)[0], self._format_time(end)[1], self._format_time(end)[2])
        step = datetime.timedelta(days=1)
        date_list = []
        while dt < end:
            date_list.append(dt.strftime('%d-%m-%Y'))
            dt += step
        return date_list

    @property
    def full_articles(self):
        return self._full_articles

    @property
    def editions(self):
        return self._editions

    @staticmethod
    def _format_time(time_string):
        time_components = time_string.split('-')
        day = int(time_components[0])
        month = int(time_components[1])
        year = int(time_components[2])
        return year, month, day

