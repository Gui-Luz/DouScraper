class ArticleChopper:

    def __init__(self, script_text_list):
        self._script_text_list = script_text_list

    def chop(self):
        articles = []
        for script_text in self._script_text_list:
            article_list = script_text['jsonArray']
            for article in article_list:
                articles.append(article)
        return articles

