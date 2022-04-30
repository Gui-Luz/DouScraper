from core.auxiliary.auxiliary import get_section, log_error, format_date, get_files_in_dir, ROOT_PATH, load_json_from_file
import json


class Sections:
    def __init__(self, edition):
        self._date = edition.date
        self._edition_sections = self._get_edition_sections(edition)
        self._scraped_sections = [edition.section_d01]
        self._extra_editions = edition.extra_editions
        self._errors = []
        self._get_sections()

    def _get_sections(self):
        if self._check_if_edition_is_saved():
            self._load_sections_from_file()
        else:
            print(f'[+][+] Will request do2, do3 and extra editions: {self._extra_editions}')
            self._save_section('do1', self._scraped_sections[0])
            for item in self._edition_sections:
                if item != 'do1':
                    print(f'[+][+] Getting {item}')
                    url = f"https://www.in.gov.br/leiturajornal?data={self._date}&secao={item}"
                    section, error = get_section(url)
                    if section:
                        print(f'---------------> Success')
                        self._save_section(item, section)
                        self._scraped_sections.append(section)
                    else:
                        print(f'---------------> Error')
                        log_error(f'[+] Could not get {self._date}: {error}')
                        self._errors.append(error)

    @property
    def sections(self):
        return self._scraped_sections

    @property
    def errors(self):
        return self._errors

    def _save_section(self, section_name, section):
        date = format_date(self._date)
        with open(f"./outputs/{date}/sections/{section_name}.json", 'a',
                    encoding='utf-8') as file:
            json.dump(section, file, indent=4, ensure_ascii=False)

    def _get_edition_sections(self, edition):
        lowercase_extra_editions = [i.lower() for i in edition.extra_editions]
        sections = set(lowercase_extra_editions)
        sections.update(['do1', 'do2', 'do3'])
        return sections

    def _check_if_edition_is_saved(self):
        print("[+][+] Checking if sections are saved:")
        files = get_files_in_dir(ROOT_PATH + f'/outputs/{format_date(self._date)}/sections')
        saved_sections = set([file.strip('.json') for file in files])
        if saved_sections == set(self._edition_sections):
            print("---------------> True")
            return True
        else:
            print("---------------> False")
            return False

    def _load_sections_from_file(self):
        for item in self._edition_sections:
            if item != 'do1':
                j = load_json_from_file(ROOT_PATH + f'/outputs/{format_date(self._date)}/sections/', f'{item}.json')
                self._scraped_sections.append(j)
