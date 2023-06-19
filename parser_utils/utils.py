from parser_utils.parser_api import HeadHunterAPI, SuperJobAPI
from parser_utils.jsonsaver import JSONSaver


def filter_vacancies(data: list, filter_words: list):
    """
    Функция получает список с вакансиями и отфильтровывает их по ключевым словам
    """
    if not filter_words:
        return data
    filtered_data = []
    for vacancy in data:
        for word in filter_words:
            if word in vacancy.job_description:
                filtered_data.append(vacancy)
                break
    return filtered_data


def sort_by_salary(data: list, num_of_top_vacancies: int = None):
    """
    Функция получает отфильтрованный список вакансий и сортирует его от
    наибольшей зарплаты к наименьшей (вакансии, у которых зарплата не указана
    в итоговой выборке будут в самом низу)
    """
    if not data:
        return []
    sorted_data = sorted(data, key=lambda x: max(x.salary), reverse=True)
    # В том случае, если в функцию не передано количество вакансий для вывода,
    # функция возвращает весь список вакансий
    if not num_of_top_vacancies:
        return sorted_data
    return sorted_data[:num_of_top_vacancies]


def check_answer(text_to_write: str, valid_answers: list) -> str:
    """
    Функция-помощник для контроля корректности вводимых пользователем данных.
    Возвращает одно из ожидаемых валидных значений для дальнейшей работы.
    """
    answer = input()
    # Проверяем находится ли введённое пользователем значение среди допустимых значений,
    # если нет - то запускается цикл while
    while answer not in valid_answers:
        print(text_to_write)
        print('Либо нажмите ENTER для завершения работы программы')
        answer = input()
        if not answer:
            print('\nРабота помощника завершена. Спасибо!')
            exit()

    return answer


def get_search_query(platforms: str, query: str, city_for_query: int = None) -> list:
    """
    Функция-помощник для запроса в API разных сайтов в зависимости от запроса пользователя.
    Возвращает список экземпляров класса Vacancy.
    """
    if platforms == '1':
        result = HeadHunterAPI().get_vacancies(query, city_for_query)
    elif platforms == '2':
        result = SuperJobAPI().get_vacancies(query, city_for_query)
    else:
        result = SuperJobAPI().get_vacancies(query, city_for_query)
        result.extend(HeadHunterAPI().get_vacancies(query, city_for_query))

    return result


def filter_helper(data: list, json_object: JSONSaver) -> None:
    """Функция-помощник для взаимодействия с пользователем после фильтрации данных"""
    print('Введите 1, если желаете обновить файл с вакансиями новыми отфильтрованными данными\n'
          'Введите 2, чтобы продолжить работу с программой')
    user_answer = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])

    # В первом случае пересохраняем данные в файл
    if user_answer == '1':
        json_object.add_vacancy(data, mode='rewrite')
