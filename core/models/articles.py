from core.auxiliary.auxiliary import get_soup, request_url, format_date_for_elk, log_error
import json
import hashlib


class Articles:

    def __init__(self, sections):
        self._sections = sections
        self._articles = self._cut_sections_into_articles()

    def _cut_sections_into_articles(self):
        articles = []
        for section in self._sections:
            article_list = section['jsonArray']
            for article in article_list:
                articles.append(article)
        return articles

    @property
    def articles(self):
        return self._articles


class FullArticles:

    def __init__(self, articles):
        self._errors = []
        self._articles = articles
        self._full_articles = []
        self._errors = []
        self._counter = 1
        self._generate_full_article()

    def _generate_full_article(self):
        print(f'[+] Will request {len(self._articles)} articles')
        for article in self._articles[:4]:                                                     ### TEST ONLY
            article = self._format_date(article)
            full_article_text = self._scrape_article_full_text(article)
            full_article = self._append_full_text_to_article(article, full_article_text)
            self._full_articles.append(full_article)
            self._save_articles(full_article)

    def _scrape_article_full_text(self, article):
        try:
            link = 'https://www.in.gov.br/web/dou/-/'
            title = article['urlTitle']
            url = link + title
            print(f'[+] {self._counter} Getting full article for {title}')
            html = request_url(url)
            soup = get_soup(html)
            full_article = soup.find("div", class_="texto-dou")
            full_article_text = full_article.text
            print(f'Success')
            self._counter += 1
            return full_article_text
        except Exception as e:
            print(f'Error')
            self._counter += 1
            log_error(f'[+] {e}')
            self._errors.append(e)

    @staticmethod
    def _append_full_text_to_article(article, full_article_text):
        article['fullText'] = full_article_text
        return article

    @staticmethod
    def _format_date(article):
        article['pubDate'] = format_date_for_elk(article['pubDate'])
        return article

    @staticmethod
    def _save_articles(article):
        hashed_string = hashlib.sha256(str(article).encode('utf-8')).hexdigest()
        with open(f"./outputs/{article['pubDate']}/full_articles/{hashed_string}.json", 'a', encoding='utf-8') as file:
            json.dump(article, file, indent=4, ensure_ascii=False)

    @property
    def full_articles(self):
        return self._full_articles
