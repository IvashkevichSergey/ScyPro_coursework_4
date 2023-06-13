import json


class Vacancy:
    def __init__(self, vacancy_name, vacancy_url, salary_from, salary_to, job_description):
        self._vacancy_name = self.check_vacancy_name(vacancy_name)
        self._salary = (salary_from if salary_from else 0, salary_to if salary_to else 0)
        self._vacancy_url = vacancy_url
        self._job_description = self.check_job_description(job_description)

    @property
    def vacancy_name(self):
        return self._vacancy_name

    @staticmethod
    def check_vacancy_name(vacancy_name):
        if not vacancy_name:
            return 'Название профессии не указано'
        return vacancy_name

    @property
    def salary(self):
        return self._salary

    @staticmethod
    def print_salary(salary_from, salary_to):
        if not salary_from and not salary_to:
            return 'Зарплата не указана'
        elif salary_to == salary_from:
            return f'{salary_to}'
        elif salary_to and not salary_from:
            return f'До {salary_to} руб.'
        elif salary_from and not salary_to:
            return f'От {salary_from} руб.'
        else:
            return f'От {salary_from} до {salary_to} руб.'

    @property
    def vacancy_url(self):
        return self._vacancy_url

    @property
    def job_description(self):
        return self._job_description

    @staticmethod
    def check_job_description(job_description):
        if not job_description:
            return 'Описание профессии не указано'
        return job_description

    def __repr__(self):
        return f'Наименование вакансии: {self.vacancy_name}\n' \
               f'Описание работы: {self.job_description}\n' \
               f'Заработная плата: {self.print_salary(*self.salary)}\n' \
               f'Ссылка на вакансию: {self.vacancy_url}\n'

    def __call__(self):
        return {
            'Наименование вакансии': self.vacancy_name,
            'Описание работы': self.job_description,
            'Заработная плата': self.print_salary(*self.salary),
            'Ссылка на вакансию': self.vacancy_url
                }

    def __lt__(self, other):
        return max(self.salary) < max(other.salary)

    def __le__(self, other):
        return max(self.salary) <= max(other.salary)

    def __eq__(self, other):
        return max(self.salary) == max(other.salary)


if __name__ == '__main__':
    with open('new_file.json', encoding='utf-8') as f:
        data = json.load(f)

    lst = []
    for item in data:
        vacancy_name = item['profession']
        vacancy_url = item['link']
        salary_from = item['payment_from']
        salary_to = item['payment_to']
        job_description = item['vacancyRichText']
        vacancy = Vacancy(vacancy_name, vacancy_url, salary_from, salary_to, job_description)
        lst.append(vacancy())

    with open('search_result.json', 'w', encoding='utf-8') as f:
        json.dump(lst, f, ensure_ascii=False, indent=4)