from parser_api import HeadHunterAPI, SuperJobAPI
from vacancies_handler import Vacancy
from jsonsaver import JSONSaver
from utils import filter_vacancies, sort_by_salary


def check_answer(text_to_write: str, valid_answers: list):
    answer = input()
    while answer not in valid_answers:
        print(text_to_write)
        print('Либо нажмите ENTER для завершения работы программы')
        answer = input()
        if not answer:
            exit()
    return answer


def get_search_query(platforms):
    search_query = input('Введите название вакансии для поиска: ')
    if platforms == '1':
        result = HeadHunterAPI().get_vacancies(search_query)
    elif platforms == '2':
        result = SuperJobAPI().get_vacancies(search_query)
    else:
        result = SuperJobAPI().get_vacancies(search_query)
        result.extend(HeadHunterAPI().get_vacancies(search_query))
    return result


def user_interaction():
    print('На какой платформе будем искать вакансии?\n'
          'Введите 1, если ищем на HeadHunter.ru\n'
          'Введите 2, если ищем на SuperJob.ru\n'
          'Введите 3, если ищем на обеих платформах')

    platforms = check_answer('Введите корректное значение: 1, 2 либо 3', ['1', '2', '3'])

    search_query = get_search_query(platforms)
    while not search_query:
        print('По Вашему запросу подходящих вакансий не найдено. Введите новый запрос для поиска.')
        print('Вы можете также не вводить ничего для завершения работы программы')
        search_query = get_search_query(platforms)
        if not search_query:
            exit()

    print('Вы желаете дополнительно указать ключевые слова для фильтрации списка доступных вакансий?\n'
          'Введите 1, если будем использовать фильтрацию по ключевым словам\n'
          'Введите 2, если в дополнительной фильтрации нет необходимости')
    use_filters = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])

    if use_filters == '1':
        keywords_list = input('Введите через пробел ключевые слова для поиска в описании вакансий: ').split()
        result = filter_vacancies(search_query, keywords_list)
        while not result:
            print('По таким ключевым словам найти ничего не удалось.\n'
                  'Введите 1, если хотите попробовать новый набор ключевых слов\n'
                  'Введите 2, если хотите продолжить без дополнительной сортировки по ключевым словам')
            use_filters = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])
            if use_filters == '1':
                keywords_list = input('Введите через пробел ключевые слова для поиска в описании вакансий: ').split()
                result = filter_vacancies(search_query, keywords_list)
            else:
                break
    else:
        result = search_query

    print('Вы желаете отсортировать итоговый список вакансий по уровню заработной платы\n'
          'Введите 1, если сортировка по заработной плате нужна\n'
          'Введите 2, если сортировку по заработной платы делать не нужно')
    sort_vacancies = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])
    if sort_vacancies == '1':
        print('В итоговый топ вакансий сохраняем все имеющиеся вакансии?\n'
              'Введите 0, если нужно сохранить все найденные вакансии\n'
              'Либо введите конкретное число вакансий для сохранения в итоговый список')
        use_top = check_answer('Необходимо ввести 0 либо любое положительное число', list(map(str, range(10000))))
        if use_top == '0':
            result = sort_by_salary(result)
        else:
            result = sort_by_salary(result, int(use_top))

    JSONSaver().add_vacancy(result, mode='rewrite')
    print('Готово! Файл "your_job_opportunity.json" с вакансиями во Вашему запросу сформирован')


if __name__ == '__main__':
    user_interaction()

