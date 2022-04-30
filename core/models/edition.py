import os
from datetime import datetime

from core.auxiliary.auxiliary import get_section, log_error, ROOT_PATH, format_date, load_json_from_file, get_files_in_dir


class Edition:

    def __init__(self, date):
        self._date = date
        self._errors = []
        self._section_d01 = self._get_section_d01()
        self._regular_edition_exists = self._verify_regular_edition_exists()
        self._extra_editions = self._find_extra_editions()

    def _get_section_d01(self):
        print(f'[+][+][+] Getting dou edition {self._date}:')
        section, error = get_section(f"https://www.in.gov.br/leiturajornal?data={self._date}&secao=do1")
        if section:
            print(f'Success')
            return section
        else:
            print(f'Error')
            log_error(f'[+] Could not get edition {self._date}: {error}')
            self._errors.append(error)

    def _verify_regular_edition_exists(self):
        print(f'[+][+][+] Checking if dou edition {self._date} exists:')
        if self._section_d01 and self._section_d01['jsonArray']:
            print(f'Exists')
            self._create_dir(self._date)
            return True
        else:
            print(f'Do not exists')
            return False

    def _find_extra_editions(self):
        if self.exists:
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

    @staticmethod
    def _create_dir(date):
        date_formated = format_date(date)
        dir_path = f"{ROOT_PATH}/outputs/{date_formated}"
        sections = dir_path + '/sections'
        articles_dir_path = dir_path + '/full_articles'
        for dir in [dir_path, sections, articles_dir_path]:
            os.makedirs(dir, exist_ok=True)

