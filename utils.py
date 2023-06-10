from parser_api import SuperJobAPI


def filtered_vacancies(data: list, filter_words: list):
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


if __name__ == '__main__':
    superjob_api = SuperJobAPI()
    superjob_vacancies = superjob_api.get_vacancies("Водитель ")
    filtered_vacancies = filtered_vacancies(superjob_vacancies, ['электроштабелер'])
    print(len(filtered_vacancies))
    for vacancy in filtered_vacancies:
        print(vacancy)



