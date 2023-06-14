from vacancies_handler import Vacancy
import json
import os


class JSONSaver:
    """Класс для сохранения данных в файл и работы с сохранёнными данными"""

    FILE_NAME = 'your_job_opportunity.json'
    PATH_TO_FILE = os.path.abspath(FILE_NAME)

    def dump_data_to_json(self, data) -> None:
        """
        Метод принимает данные и загружает их в файл
        """
        with open(self.FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data_from_json(self) -> list:
        """
        Метод открывает файл на чтение и возвращает данные из этого файла
        """
        with open(self.FILE_NAME, encoding='utf-8') as f:
            data = json.load(f)
        return data

    def add_vacancy(self, list_of_vacancies: list, mode: str = None) -> None:
        """
        Метод принимает список с вакансиями и записывает их в файл.
        Если передан режим 'rewrite', то существующий файл перезаписывается
        """
        vacancies_to_save = [vacancy() for vacancy in list_of_vacancies]
        if not os.path.isfile(self.PATH_TO_FILE) or mode == 'rewrite':
            self.dump_data_to_json(vacancies_to_save)
        else:
            data = self.load_data_from_json()
            data.extend(vacancies_to_save)
            self.dump_data_to_json(data)

    def get_vacancy(self) -> list:
        """
        Метод загружает из файла все вакансии, оборачивает каждую вакансию в объект
        класса Vacancy и возвращает список c этими объектами
        """
        loaded_data = []
        data = self.load_data_from_json()
        for vacancy in data:
            salary = self.get_salary_for_vacancy_object(vacancy['Заработная плата'])
            loaded_data.append(Vacancy(vacancy_name=vacancy['Наименование вакансии'],
                                       vacancy_url=vacancy['Ссылка на вакансию'],
                                       salary_from=salary[0],
                                       salary_to=salary[1],
                                       job_description=vacancy['Описание работы']))
        return loaded_data

    @staticmethod
    def get_salary_for_vacancy_object(salary_string: str) -> tuple:
        """
        Статичный метод для формирования корректных данных из строки с зарплатой для объекта класса Vacancy.
        Возвращает кортеж из двух чисел.
        """
        split_string = salary_string.split()
        if len(split_string) == 1:
            return int(salary_string), int(salary_string)
        if salary_string == 'Зарплата не указана':
            return 0, 0
        if salary_string.startswith('От') and len(split_string) == 3:
            return int(split_string[1]), 0
        if salary_string.startswith('До') and len(split_string) == 3:
            return 0, int(split_string[1])
        return int(split_string[1]), int(split_string[3])

    def get_vacancy_by_salary(self, salary_from: int) -> list:
        """
        Метод отсекает вакансии ниже указанной зарплате.
        Возвращает список с отфильтрованными по зарплате вакансиями.
        """
        all_vacancies = self.get_vacancy()
        vacancies_filtered_by_salary = []
        for vacancy in all_vacancies:
            if max(vacancy.salary) >= salary_from:
                vacancies_filtered_by_salary.append(vacancy)
        return vacancies_filtered_by_salary

    def delete_vacancy_by_keywords(self, keywords: str) -> list:
        """
        Метод принимает строку с ключевыми словами, проверяет наличие этих слов в описании либо названии каждой
        вакансии и оставляет только те вакансии, в которых ключевые слова не встречаются.
        Возвращает список с отфильтрованными вакансиями.
        """
        keywords = keywords.split()
        list_with_vacancies = self.get_vacancy()
        vacancies_to_delete = []
        for vacancy in list_with_vacancies:
            for word in keywords:
                if word in vacancy.vacancy_name or word in vacancy.job_description:
                    vacancies_to_delete.append(vacancy.vacancy_url)
                    break

        return [vacancy for vacancy in list_with_vacancies if vacancy.vacancy_url not in vacancies_to_delete]

