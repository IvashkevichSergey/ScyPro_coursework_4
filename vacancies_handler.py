class Vacancy:
    """
    Класс для работы с вакансиями, поддерживает работу с параметрами: название вакансии,
    ссылка на вакансию, зарплата, описание вакансии
    """
    def __init__(self, vacancy_name, vacancy_url, salary_from, salary_to, job_description):
        self._vacancy_name = self.check_vacancy_name(vacancy_name)
        self._salary = (salary_from if salary_from else 0, salary_to if salary_to else 0)
        self._vacancy_url = vacancy_url
        self._job_description = self.check_job_description(job_description)

    @property
    def vacancy_name(self) -> str:
        """Геттер для атрибута vacancy_name"""
        return self._vacancy_name

    @staticmethod
    def check_vacancy_name(vacancy_name: str):
        """Метод для проверки на валидность атрибута vacancy_name"""
        if not vacancy_name:
            return 'Название профессии не указано'
        return vacancy_name

    @property
    def salary(self) -> tuple:
        """Геттер для атрибута salary"""
        return self._salary

    @staticmethod
    def print_salary(salary_from: int, salary_to: int)  -> str:
        """Метод возвращает атрибут salary в корректном виде для передачи в __repr__"""
        if not salary_from and not salary_to:
            return 'Зарплата не указана'
        if salary_to == salary_from:
            return f'{salary_to}'
        if salary_to and not salary_from:
            return f'До {salary_to} руб.'
        if salary_from and not salary_to:
            return f'От {salary_from} руб.'
        return f'От {salary_from} до {salary_to} руб.'

    @property
    def vacancy_url(self) -> str:
        """Геттер для атрибута vacancy_url"""
        return self._vacancy_url

    @property
    def job_description(self) -> str:
        """Геттер для атрибута job_description"""
        return self._job_description

    @staticmethod
    def check_job_description(job_description: str) -> str:
        """Метод для проверки на валидность атрибута check_job_description"""
        if not job_description:
            return 'Описание профессии не указано'
        return job_description

    def __repr__(self) -> str:
        return f'Наименование вакансии: {self.vacancy_name}\n' \
               f'Описание работы: {self.job_description}\n' \
               f'Заработная плата: {self.print_salary(*self.salary)}\n' \
               f'Ссылка на вакансию: {self.vacancy_url}\n'

    def __call__(self) -> dict:
        return {
            'Наименование вакансии': self.vacancy_name,
            'Описание работы': self.job_description,
            'Заработная плата': self.print_salary(*self.salary),
            'Ссылка на вакансию': self.vacancy_url
        }

    def __lt__(self, other) -> bool:
        return max(self.salary) < max(other.salary)

    def __le__(self, other) -> bool:
        return max(self.salary) <= max(other.salary)

    def __eq__(self, other) -> bool:
        return max(self.salary) == max(other.salary)


if __name__ == '__main__':
    pass
