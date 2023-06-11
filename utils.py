from parser_api import SuperJobAPI
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


def sort_by_salary(data: list, num_of_top_vacancies: int):
    """
    Функция получает отфильтрованный список вакансий и сортирует его от
    наибольшей зарплаты к наименьшей (вакансии, у которых зарплата не указана
    в итоговой выборке будут в самом низу
    """
    if not data:
        return []
    return sorted(data, key=lambda x: max(x.salary), reverse=True)[:num_of_top_vacancies]


if __name__ == '__main__':
    superjob_api = SuperJobAPI()
    superjob_vacancies = superjob_api.get_vacancies("контролер")
    filtered_vacancies = filter_vacancies(superjob_vacancies, [])
    sorted_vacancies = sort_by_salary(filtered_vacancies, 10)
    # print(len(filtered_vacancies))
    # for vacancy in sorted_vacancies:
    #     print(vacancy)
    json_saver = JSONSaver()
    json_saver.add_vacancy(sorted_vacancies)
    # data = json_saver.get_vacancy()
    # for el in data:
    #     print(el.vacancy_name, el.print_salary(*el.salary))





