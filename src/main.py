from src.classes import HH_Vacancies_API, Json_HH, SJ_Vacancies_API, Currency_API, Json_SJ
from src.utils import sort_by_min_salary, sort_by_max_salary, top_10_by_salary, choose_platform, choose_option

if __name__ == '__main__':

    search_platform = choose_platform()

    keyword = input("Введите ключевое слово для поиска вакансий:  ")

    if search_platform == '1':
        hh = HH_Vacancies_API() #Создание экземпляра класса для работы с API сайтов с вакансиями
        hh_vacancies = hh.get_vacancies(keyword)
        hh_json = Json_HH(keyword)
        hh_json.add_vacancies(hh_vacancies)
        data = hh_json.select()
    else:
        sj = SJ_Vacancies_API()
        sj_vacancies = sj.get_vacancies(keyword)
        sj_json = Json_SJ(keyword)
        sj_json.add_vacancies(sj_vacancies)
        data = sj_json.select()

    action = choose_option()

    print(f"\n\n{'*' * 200}\n\n")

    if action == "1":
        data = sort_by_min_salary(data)
        for item in data:
            print(item, end=f"\n\n{'*' * 200}\n\n")
    elif action == '2':
        data = sort_by_max_salary(data)
        for item in data:
            print(item, end=f"\n\n{'*' * 200}\n\n")
    else:
        data = top_10_by_salary(data)













