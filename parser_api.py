import os
from abc import ABC, abstractmethod
import requests
from pprint import pprint
import json
from vacancies_handler import Vacancy


class ParserAPI(ABC):
    pass


class SuperJobAPI(ParserAPI):
    # Словарь с параметрами для получения токена
    _params = {
        'code': '5bce8afac323d5103bdec5427f780e2019954e12256c7524dd9586e0ba59e511.8a408c62156de2c1259c58bd3629b52dc3f3ad99',
        'redirect_uri': 'http://www.example.ru',
        'client_id': 2551,
        'client_secret': 'v3.r.131331406.ddf3dd48314bb05b354e7a90398237055723873f.571b102b302047db1cdd5d3bc7d20bdfc348337f'}

    def __init__(self):
        self.access_token = self.get_token()
        self.headers = {'Host': 'api.superjob.ru',
                        'X-Api-App-Id': SuperJobAPI._params['client_secret'],
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/x-www-form-urlencoded'
                        }

    @staticmethod
    def get_token():
        """
        Статичный метод для получения токена в том случае, если он ещё не получен
        """
        # Если файл с токеном не существует, запрашиваем его один раз
        if not os.path.isfile('config.json'):
            response = requests.get('https://api.superjob.ru/2.0/oauth2/access_token/',
                                    params=SuperJobAPI._params).json()
            # Словарь с токеном сохраняем в отдельный файл
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=2)

        # Получаем значение токена из файла
        with open('config.json', encoding='utf-8') as f:
            data = json.load(f)
            return data['access_token']

    def get_vacancies(self, vacancy):
        """
        Метод для формирования файла со списком вакансий по ключевому слову
        """
        # Создаём временную переменную для хранения словарей с вакансиями
        data = []
        # Словарь с параметрами для поискового запроса
        params = {'keyword': vacancy,
                  'count': 100,
                  'page': 0}
        request = requests.get('https://api.superjob.ru/2.0/vacancies/',
                               params=params, headers=self.headers).json()

        # Если вакансий не найдено - завершаем работу функции
        if not request['objects']:
            print('Вакансий по такому запросу не найдено')
            return []

        # Проходим по всем страницам с искомым запросом и сохраняем все вакансии в список
        while request['objects'] and params['page'] < 5:
            print(params['page'] + 1, '--->', len(request['objects']))
            for vacancy in request['objects']:
                data.append(Vacancy(vacancy_name=vacancy['profession'],
                                    vacancy_url=vacancy['link'],
                                    salary_from=vacancy['payment_from'],
                                    salary_to=vacancy['payment_to'],
                                    job_description=vacancy['candidat']))
            params['page'] += 1
            request = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                   params=params, headers=self.headers).json()

        # Записываем все найденные вакансии в новый файл
        # with open('new_file.json', 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=2)

        # with open('new_file.json', 'r', encoding='utf-8') as f:
        #     print(len(json.load(f)))

        return data


class HeadHunterAPI(ParserAPI):
    pass


if __name__ == '__main__':
    superjob_api = SuperJobAPI()
    superjob_vacancies = superjob_api.get_vacancies("python разработчик")
    for i in superjob_vacancies:
        print(i)
        print('>>>>>>>>>>>>>>>>>>>>>')

    print(superjob_vacancies[0] > superjob_vacancies[1])
    print(superjob_vacancies[1] <= superjob_vacancies[2])
    print(superjob_vacancies[2] < superjob_vacancies[3])
    print(superjob_vacancies[3] == superjob_vacancies[4])
    print(superjob_vacancies[4] >= superjob_vacancies[5])

# response = requests.get('https://api.superjob.ru/2.0/vacancies/?keyword=Python&Java&count=100&page=6', headers=headers).json()
