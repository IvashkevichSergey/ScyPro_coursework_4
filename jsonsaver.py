import json
from vacancies_handler import Vacancy
import os


class JSONSaver:
    FILE_NAME = 'your_job_opportunity.json'
    PATH_TO_FILE = os.path.abspath(FILE_NAME)

    @staticmethod
    def dump_data_to_json(data):
        with open(JSONSaver.FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_data_from_json():
        with open(JSONSaver.FILE_NAME, encoding='utf-8') as f:
            data = json.load(f, ensure_ascii=False, indent=2)
        return data

    @staticmethod
    def add_vacancy(list_of_vacancies):
        vacancies_to_save = [vacancy() for vacancy in list_of_vacancies]
        if not os.path.join(JSONSaver.PATH_TO_FILE, JSONSaver.FILE_NAME):
            JSONSaver.dump_data_to_json(vacancies_to_save)
        else:
            data = JSONSaver.load_data_from_json()
            data.extend(vacancies_to_save)
            JSONSaver.dump_data_to_json(data)

    @staticmethod
    def get_vacancy():
        loaded_data = []
        data = JSONSaver.load_data_from_json()
        for vacancy in data:
            salary = JSONSaver.get_salary_for_vacancy_object(vacancy['Заработная плата'])
            loaded_data.append(Vacancy(vacancy_name=vacancy['Наименование вакансии'],
                                       vacancy_url=vacancy['Ссылка на вакансию'],
                                       salary_from=salary[0],
                                       salary_to=salary[1],
                                       job_description=vacancy['Описание работы']))
        return loaded_data

    @staticmethod
    def get_salary_for_vacancy_object(salary_string: str):
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
