import os
from abc import ABC, abstractmethod
import requests
import json
from vacancies_handler import Vacancy


class ParserAPI(ABC):
    """
    Абстрактный класс для работы с API различных сайтов с вакансиями
    """
    @abstractmethod
    def get_vacancies(self, vacancy_name):
        pass


class SuperJobAPI(ParserAPI):
    """Класс для работы с API сайта superjob.ru"""

    CONFIG_FILE = os.path.abspath('config_files/SJru_config.json')

    def __init__(self):
        self.headers = {'Host': 'api.superjob.ru',
                        'X-Api-App-Id': 'v3.r.131331406.ddf3dd48314bb05b354e7a90398237055723873f.571b102b302047db1cdd5d3bc7d20bdfc348337f',
                        'Authorization': f'Bearer {self.get_token()}',
                        'Content-Type': 'application/x-www-form-urlencoded'
                        }

    def get_token(self) -> str:
        """Метод возвращает значение токена"""
        with open(self.CONFIG_FILE, encoding='utf-8') as config_file:
            return json.load(config_file)['access_token']

    def refresh_token(self) -> None:
        """
        Метод для обновления токена в том случае, если при запросе на API получена ошибка 410
        """
        # Получаем значение refresh токена из файла
        with open(self.CONFIG_FILE, encoding='utf-8') as config_file:
            refresh_token = json.load(config_file)['refresh_token']

        # Создаём новый словарь с параметрами для отправки на API
        refresh_params = {
            'refresh_token': refresh_token,
            'client_id': 2551,
            'client_secret': self.headers['X-Api-App-Id']
        }

        # Выполняем запрос на обновление токена
        response_for_new_token = requests.get('https://api.superjob.ru/2.0/oauth2/refresh_token/',
                                              params=refresh_params).json()
        # Словарь с токеном пересохраняем в файл
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as config_file:
            json.dump(response_for_new_token, config_file, ensure_ascii=False, indent=2)

        # Обновляем токен в словаре headers
        self.headers['Authorization'] = f'Bearer {response_for_new_token["access_token"]}'

    def get_vacancies(self, vacancy):
        """Метод для формирования файла со списком вакансий по ключевому слову"""
        # Словарь с параметрами для поискового запроса
        search_params = {'keyword': vacancy,
                         'count': 100,
                         'page': 0}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                params=search_params, headers=self.headers).json()

        # Если ответом сервера стала ошибка 410, то запускаем функцию обновления токена
        # и повторно запускаем функцию get_vacancies
        if response.get('error'):
            if response.get('error').get('code') == 410:
                self.refresh_token()
                return self.get_vacancies(vacancy)

        # Если вакансий не найдено - функция возвращает пустой список
        if not response['objects']:
            print('Вакансий по такому запросу не найдено')
            return []

        # Создаём переменную для хранения вакансий - объектов класса Vacancy
        data = []
        # Проходим по всем страницам с искомым запросом и сохраняем все вакансии в список
        while response['objects'] and search_params['page'] < 5:
            print(search_params['page'] + 1, '--->', len(response['objects']))
            for vacancy in response['objects']:
                data.append(Vacancy(vacancy_name=vacancy['profession'],
                                    vacancy_url=vacancy['link'],
                                    salary_from=vacancy['payment_from'],
                                    salary_to=vacancy['payment_to'],
                                    job_description=vacancy['candidat']))
            search_params['page'] += 1
            response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                   params=search_params, headers=self.headers).json()
        print(len(data))
        return data


class HeadHunterAPI(ParserAPI):
    """Класс для работы с API сайта hh.ru"""
    def get_vacancies(self, vacancy):
        """
        Метод для формирования файла со списком вакансий по ключевому слову
        """
        # Словарь с параметрами для поискового запроса
        search_params = {'text': vacancy,
                         'per_page': 100,
                         'page': 0}

        response = requests.get('https://api.hh.ru/vacancies', params=search_params).json()

        # Если вакансий не найдено - функция возвращает пустой список
        if not response['items']:
            print('Вакансий по такому запросу не найдено')
            return []

        # Создаём переменную для хранения вакансий - объектов класса Vacancy
        data = []
        # Проходим по всем страницам с искомым запросом и сохраняем все вакансии в список
        while search_params['page'] < 20 and response['items']:
            print(search_params['page'] + 1, '--->', len(response['items']))
            # with open('temp.json', 'w', encoding='utf-8') as f:
            #     json.dump(response['items'], f, ensure_ascii=False, indent=2)
            for vacancy in response['items']:
                data.append(Vacancy(vacancy_name=vacancy['name'],
                                    vacancy_url=vacancy['alternate_url'],
                                    salary_from=None if not vacancy.get('salary') else vacancy.get('salary').get(
                                        'from'),
                                    salary_to=None if not vacancy.get('salary') else vacancy.get('salary').get('to'),
                                    job_description=vacancy['snippet']['responsibility']))
            search_params['page'] += 1
            response = requests.get('https://api.hh.ru/vacancies', params=search_params).json()
        print(len(data))
        return data


if __name__ == '__main__':
    pass
