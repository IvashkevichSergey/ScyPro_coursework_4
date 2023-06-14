from parser_api import SuperJobAPI, HeadHunterAPI
from jsonsaver import JSONSaver


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


if __name__ == '__main__':
    # superjob_api = SuperJobAPI()
    # superjob_vacancies = superjob_api.get_vacancies("кассир")
    # filtered_vacancies = filter_vacancies(superjob_vacancies, [])
    # sorted_vacancies = sort_by_salary(filtered_vacancies, 10)
    # print(len(filtered_vacancies))
    # for vacancy in sorted_vacancies:
    #     print(vacancy)

    # # data = json_saver.get_vacancy()
    # # for el in data:
    # #     print(el.vacancy_name, el.print_salary(*el.salary))
    # res = json_saver.delete_vacancy_by_keywords('бульдозер')
    headhunter_api = SuperJobAPI()
    headhunter_vacancies = headhunter_api.get_vacancies("машинист")
    filtered_vacancies = filter_vacancies(headhunter_vacancies, ['трактор', 'экскаватор'])
    print(len(filtered_vacancies))
    sorted_vacancies = sort_by_salary(filtered_vacancies, 25)
    print(len(sorted_vacancies))
    json_saver = JSONSaver()
    json_saver.add_vacancy(sorted_vacancies, mode='rewrite')
    # for item in sorted_vacancies:
    #     print(item)
    #     print('-' * 50)







