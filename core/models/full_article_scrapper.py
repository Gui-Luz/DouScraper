from core.auxiliary.auxiliary import get_soup, request_url


class FullArticleScraper:

    def __init__(self, article):
        self._errors = []
        self._article = article
        self._url_title = self._article['urlTitle']
        self._full_link = self._link_finder()
        self._article_text = self._get_full_article()

    def _link_finder(self):
        link = 'https://www.in.gov.br/web/dou/-/'
        full_link = link + self._url_title
        return full_link

    def _get_full_article(self):
        try:
            html = request_url(self._full_link)
            soup = get_soup(html)
            full_article = soup.find("div", class_="texto-dou")
            article_text = full_article.text
            return article_text
        except:
            self._errors.append(self._full_link)

    def return_full_article(self):
        self._article['fullText'] = self._article_text
        return self._article
