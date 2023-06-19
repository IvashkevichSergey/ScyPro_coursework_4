from parser_utils.parser_api import HeadHunterAPI, SuperJobAPI
from parser_utils.jsonsaver import JSONSaver
from parser_utils.utils import filter_vacancies, sort_by_salary, check_answer, get_search_query, filter_helper


def user_interaction_with_raw_data() -> list:
    """Функция для взаимодействия с пользователем на стадии получения данных с API
    и их предварительной фильтрации и сортировки.
    Возвращает список вакансий"""
    print('На какой платформе будем искать вакансии?\n'
          'Введите 1, если ищем на HeadHunter.ru\n'
          'Введите 2, если ищем на SuperJob.ru\n'
          'Введите 3, если ищем на обеих платформах')

    platforms = check_answer('Введите корректное значение: 1, 2 либо 3', ['1', '2', '3'])
    print('\nВведите название вакансии для поиска:', end=' ')
    search_query = input()

    print('\nВ каком городе будем искать вакансии?\n'
          'Введите 1, если ищем по всей России и доступным странам СНГ\n'
          'Либо введите полное название города либо области, по которым желаете найти доступные вакансии')
    city_for_query = input()

    # Если ни на hh.ru, ни на sj.ru введённый пользователем город не найден, то программа запросит другой город,
    # либо введённая цифра "1" приведёт к поиску по всем городам
    if city_for_query != '1':
        while city_for_query != '1' and \
                not HeadHunterAPI.check_city(city_for_query) and \
                not SuperJobAPI.check_city(city_for_query):
            print(f'Населённого пункта с названием "{city_for_query}" найти не удалось...'
                  f'Проверьте правильность написания населённого пункта '
                  f'либо введите 1 для поиска по всей России и доступным странам СНГ')
            city_for_query = input()

    # Для поиска по всем городам перезаписываем цифру "1" в None
    city_for_query = None if city_for_query == '1' else city_for_query

    # По заданным вопросам запускаем поиск вакансий. Если вакансий не найдено, то
    # программа запросит другой поисковый запрос
    answer_to_query = get_search_query(platforms, search_query, city_for_query)
    while not answer_to_query:
        print('По Вашему запросу подходящих вакансий не найдено. Введите новый запрос для поиска.')
        print('Вы можете также не вводить ничего для завершения работы программы')
        search_query = input()
        # Если пользователь ничего не ввёл - завершаем работу программы
        if not search_query:
            print('\nРабота помощника завершена. Спасибо!')
            exit()
        answer_to_query = get_search_query(platforms, search_query, city_for_query)

    # По желанию пользователя делаем дополнительную фильтрацию выборки вакансий по ключевым словам
    print('\nВы желаете дополнительно указать ключевые слова для фильтрации списка доступных вакансий?\n'
          'Введите 1, если будем использовать фильтрацию по ключевым словам\n'
          'Введите 2, если в дополнительной фильтрации нет необходимости')
    use_filters = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])

    # Запрашиваем у пользователя список слов для фильтрации вакансий. Если по данным словам фильтрация
    # не дала результатов, то повторно запрашиваем список ключевых слов.
    # Если фильтрация не требуется - программа идёт дальше
    if use_filters == '1':
        keywords_list = input('Введите через пробел ключевые слова для поиска в описании вакансий: ').split()
        result = filter_vacancies(answer_to_query, keywords_list)
        while not result:
            print('По таким ключевым словам найти ничего не удалось.\n'
                  'Введите 1, если хотите попробовать новый набор ключевых слов\n'
                  'Введите 2, если хотите продолжить без дополнительной сортировки по ключевым словам')
            use_filters = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])
            if use_filters == '1':
                keywords_list = input('Введите через пробел ключевые слова для поиска в описании вакансий: ').split()
                result = filter_vacancies(answer_to_query, keywords_list)
            else:
                break
    else:
        result = answer_to_query

    # По желанию пользователя делаем сортировку выборки вакансий по зарплате
    print('\nВы желаете отсортировать итоговый список вакансий по уровню заработной платы\n'
          'Введите 1, если сортировка по заработной плате нужна\n'
          'Введите 2, если сортировку по заработной платы делать не нужно')
    sort_vacancies = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])

    # Если требуется сортировка вакансий по зарплате, то запрашиваем у пользователя также
    # дополнительный параметр сортировки - количество вакансий, выводимых в итоговом списке
    if sort_vacancies == '1':

        print('В итоговый топ вакансий сохраняем все имеющиеся вакансии?\n'
              'Введите 0, если нужно сохранить все найденные вакансии\n'
              'Либо введите конкретное число вакансий для сохранения в итоговый список')
        use_top = check_answer('Необходимо ввести 0 либо любое положительное число', list(map(str, range(10000))))
        if use_top == '0':
            result = sort_by_salary(result)
        else:
            result = sort_by_salary(result, int(use_top))

    return result


def user_interaction_with_saved_data(jsonclass_object: JSONSaver) -> None:
    """Функция для взаимодействия с пользователем на стадии получения сохранённых данных
    из json файла и их обработки. Принимает объект класса JSONSaver."""
    print('Выберите дальнейшее действие\n'
          'Введите 1, если желаете вывести весь список сохранённых вакансий на экран\n'
          'Введите 2, если желаете отфильтровать вакансии по уровню заработной платы\n'
          'Введите 3, если желаете удалить вакансии, содержащие ключевые слова\n'
          'Введите 4, если желаете добавить новые вакансии по новому запросу в имеющуюся выборку вакансий\n'
          'Для завершения работы программы введите 0')

    user_answer = check_answer('Введите корректное значение: 0, 1, 2, 3 либо 4', ['0', '1', '2', '3', '4'])
    if user_answer == '0':
        print('\nРабота помощника завершена. Спасибо!')
        exit()

    # Для получения списка всех сохранённых вакансий из json файла используем соответствующий метод
    elif user_answer == '1':
        data = jsonclass_object.get_all_vacancies()
        for vacancy in data:
            print(vacancy)
        print('\nРабота помощника завершена. Спасибо!')
        exit()

    elif user_answer == '2':
        print('Введите значение заработной платы, ниже которой вакансии Вам не интересны:', end=' ')
        salary = input()
        # Проводим валидацию введённых пользователем данных
        while not salary.isdigit() or int(salary) <= 0:
            print('Неплохо было бы ввести корректное положительное число для корректной фильтрации '
                  'вакансий по уровню заработной платы')
            salary = input()
        # Соответствующий метод класса JSONSaver производит фильтрацию данных по минимальной
        # заработной плате
        data = jsonclass_object.get_vacancy_by_salary(int(salary))
        filter_helper(data, jsonclass_object)

    elif user_answer == '3':
        keywords_list = input('Введите через пробел ключевые слова, '
                              'вакансии с которыми следует удалить из подборки: ').split()
        # Соответствующий метод класса JSONSaver производит удаление вакансий по ключевым словам
        data = jsonclass_object.delete_vacancy_by_keywords(keywords_list)
        # Если после удаления вакансий не осталось - просто запускаем работу с файлом json с начала
        if not data:
            print('По таким ключевым словам в итоговой выборке у нас не осталось ничего...')
            return user_interaction_with_saved_data(jsonclass_object)
        filter_helper(data, jsonclass_object)

    else:
        # По желанию пользователя проводим повторный запрос вакансий с API
        repeated_query = user_interaction_with_raw_data()
        # Добавляем найденные вакансии в json файл
        jsonclass_object.add_vacancy(repeated_query)
        print('Готово! Файл "your_job_opportunity.json" обновлён вакансиями из нового запроса\n')
        print('Введите 1, если хотите применить сортировку всех вакансий в файле по уровню заработной платы\n'
              'Введите 2, если хотите продолжить без сортировки по уровню заработной платы')
        use_filters = check_answer('Введите корректное значение: 1 либо 2', ['1', '2'])

        if use_filters == '1':
            all_vacancies = jsonclass_object.get_all_vacancies()
            sorted_data = sort_by_salary(all_vacancies)
            jsonclass_object.add_vacancy(sorted_data, mode='rewrite')
    # Повторно запускаем цикл работы с json файлом до тех пор, пока пользователь либо не введёт "0",
    # либо не запросит вывод данных в консоль
    return user_interaction_with_saved_data(jsonclass_object)


if __name__ == '__main__':
    # Цикл работы с программой - получение данных с API и из предобработка ->
    # сохранение данных в json файл ->
    # цикл работы с сохранёнными данными.
    vacancies_by_query = user_interaction_with_raw_data()
    json_saver = JSONSaver()
    json_saver.add_vacancy(vacancies_by_query, mode='rewrite')
    print('Готово! Файл "your_job_opportunity.json" с вакансиями во Вашему запросу сформирован\n')
    user_interaction_with_saved_data(json_saver)
