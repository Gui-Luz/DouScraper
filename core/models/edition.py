from core.auxiliary.auxiliary import get_section, log_error


class Edition:

    def __init__(self, date):
        self._date = date
        self._section_d01 = self._get_section_d01()
        self._regular_edition_exists = self._verify_regular_edition_exists()
        self._extra_editions = self._find_extra_editions()
        self._errors = []

    def _get_section_d01(self):
        print(f'[+][+][+] Getting dou edition {self._date}:')
        section, error = get_section(f"https://www.in.gov.br/leiturajornal?data={self._date}&secao=do1")
        if section:
            print(f'Success')
            return section
        else:
            print(f'Error')
            log_error(f'[+] Could not get {self._date}: {error}')
            self._errors.append(error)

    def _verify_regular_edition_exists(self):
        print(f'[+][+][+] Checking if dou edition {self._date} exists:')
        if self._section_d01['jsonArray']:
            print(f'Exists')
            return True
        else:
            print(f'Do not exists')
            return False

    def _find_extra_editions(self):
        extra_editions = []
        self._sections_info = self._section_d01['typeNormDay']
        for key in self._sections_info:
            if self._sections_info[key]:
                extra_editions.append(key)
        return extra_editions


    @property
    def errors(self):
        return self._errors

    @property
    def date(self):
        return self._date

    @property
    def section_d01(self):
        return self._section_d01

    @property
    def extra_editions(self):
        return self._extra_editions

    @property
    def exists(self):
        return self._regular_edition_exists
