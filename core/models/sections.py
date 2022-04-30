from core.auxiliary.auxiliary import get_section, log_error


class Sections:
    def __init__(self, edition):
        self._date = edition.date
        self._sections = [edition.section_d01]
        self._extra_editions = edition.extra_editions
        self._errors = []
        self._get_sections()

    def _get_sections(self):
        print(f'[+][+] Will request d02, d03 and extra editions: {self._extra_editions}')
        for item in ['do2', 'do3']:
            print(f'[+][+] Getting {item}')
            url = f"https://www.in.gov.br/leiturajornal?data={self._date}&secao={item}"
            section, error = get_section(url)
            if section:
                print(f'Success')
                self._sections.append(section)
            else:
                print(f'Error')
                log_error(f'[+] Could not get {self._date}: {error}')
                self._errors.append(error)
        for item in self._extra_editions:
            print(f'[+][+] Getting {item}')
            section = item.lower()
            url = f'https://www.in.gov.br/leiturajornal?data={self._date}&secao={section}'
            section, error = get_section(url)
            if section:
                print(f'Success')
                self._sections.append(section)
            else:
                print(f'Error')
                log_error(f'[+] Could not get {self._date}: {error}')
                self._errors.append(error)

    @property
    def sections(self):
        return self._sections

    @property
    def errors(self):
        return self._errors
