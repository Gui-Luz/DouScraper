import json
from core.auxiliary.auxiliary import get_soup, request_url


class EditionBuilder:

    def __init__(self, date):
        self._errors = []
        self._date = date
        self._script_text = self._get_script_text(f"https://www.in.gov.br/leiturajornal?data={self._date}&secao=do1")
        self._regular_edition_exists = self._verify_regular_edition_exists()
        self._extra_editions = self._find_extra_editions()

    def _get_script_text(self, url):
        try:
            html = request_url(url)
            soup = get_soup(html)
            script_result = self._find_script_result(soup)
            return script_result
        except:
            self._errors.append(url)

    def _verify_regular_edition_exists(self):
        if self._script_text['jsonArray']:
            return True
        else:
            return False

    def _find_extra_editions(self):
        extra_editions = []
        self._sections_info = self._script_text['typeNormDay']
        for key in self._sections_info:
            if self._sections_info[key]:
                extra_editions.append(key)
        return extra_editions

    def builder(self):
        script_texts = []
        if self._regular_edition_exists:
            script_texts.append(self._script_text)
            for item in ['do1' 'do2']:
                url = f"https://www.in.gov.br/leiturajornal?data={self._date}&secao={item}"
                try:
                    script_texts.append(self._get_script_text(url))
                except:
                    self._errors.append(url)
        for item in self._extra_editions:
            section = item.lower()
            url = f'https://www.in.gov.br/leiturajornal?data={self._date}&secao={section}'
            try:
                script_texts.append(self._get_script_text(url))
            except:
                self._errors.append(url)
        return script_texts

    @staticmethod
    def _find_script_result(soup):
        script = soup.find("script", id="params")
        return json.loads(script.text)

    def get_errors(self):
        return self._errors
