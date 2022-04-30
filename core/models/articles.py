from core.auxiliary.auxiliary import get_soup, request_url, format_date_for_elk, log_error, get_files_in_dir
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
        self._counter = 0
        self._generate_full_article()

    def _generate_full_article(self):
        print(f'[+] {len(self._articles)} articles found in edition')
        for article in self._articles:
            self._counter += 1
            print(f"[+] {self._counter} Article: {article['urlTitle']}")
            article = self._format_date(article)
            hashed_article = hashlib.sha256(str(article).encode('utf-8')).hexdigest()
            if not self._check_article_is_saved(article, hashed_article):
                full_article_text = self._scrape_article_full_text(article)
                full_article = self._append_full_text_to_article(article, full_article_text)
                self._full_articles.append(full_article)
                self._save_article(full_article, hashed_article)

    def _scrape_article_full_text(self, article):
        try:
            print(f'---------------> Requesting article...')
            link = 'https://www.in.gov.br/web/dou/-/'
            title = article['urlTitle']
            url = link + title
            html = request_url(url)
            soup = get_soup(html)
            full_article = soup.find("div", class_="texto-dou")
            full_article_text = full_article.text
            print(f'---------------> Success')
            return full_article_text
        except Exception as e:
            print(f'---------------> Error')
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
    def _save_article(article, hashed_article):
        with open(f"./outputs/{article['pubDate']}/full_articles/{hashed_article}.json", 'a', encoding='utf-8') as file:
            json.dump(article, file, indent=4, ensure_ascii=False)

    @property
    def full_articles(self):
        return self._full_articles

    @staticmethod
    def _check_article_is_saved(article, hashed_article):
        files = get_files_in_dir(f"./outputs/{article['pubDate']}/full_articles/")
        if hashed_article in [file.strip('.json') for file in files]:
            print(f'---------------> Article is already saved')
            return True
        else:
            print(f'---------------> Article is not yet saved')
            return False



