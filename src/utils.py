def choose_platform():
    """ Функция для выбора платфомы для поиска вакансий"""

    search_platform = input("Выберите платформу для поиска вакансий. \n"
                                "Укажите: 1 - для поиска на HeadHunter, \n"
                                "2 - для поиска наSuperJob:  ")
    if search_platform not in ['1', '2']:
        print("Указанная платформа недоступна для поиска")
        return choose_platform()
    else:
        return search_platform


def choose_option():
    """ Функция для выбора вывода вакансий на экран"""

    action = input("Выберите дальнейшие действия: 1 - смотреть вакансии, отсортированные по мин зарплате, \n"
                  "2 - смотреть вакансии, отсортированные по максимальной зарплате, \n"
                  "3 - топ 10 вакансий по зарплате  ")
    if action not in ['1', '2', '3']:
        print("Выбранная опция не поддерживается")
        return choose_option()
    else:
        return action


def sort_by_min_salary(data):
    """ Функция для сортировки вакансий по минимальной зарплате"""

    min_salary = sorted(data, reverse=True)
    return min_salary


def sort_by_max_salary(data):
    """ Функция для сортировки вакансий по максимальной зарплате"""

    max_salary = sorted(data, key=lambda x: (x.salary_sort_max is not None, x.salary_sort_max), reverse=True)
    return max_salary


def top_10_by_salary(data):

    """ Функция для получения топ 10 вакансий исходя из минимально указанной зарплаты"""

    min_salary = sorted(data, reverse=True)
    for item in min_salary[:10]:
        print(item, end=f"\n\n{'*' * 200}\n\n")

