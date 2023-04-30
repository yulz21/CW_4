import requests
import json
import os
from abc import ABC, abstractmethod
from pprint import pprint

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')


class API_Data(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_data(self, **args):
        pass


class HH_Vacancies_API(API_Data):
    """Класс для получения информации по вакансиям из HH"""

    url = 'https://api.hh.ru/vacancies'

    def get_data(self, keyword: str, page: int):
        params = {"page": page,
                  "per_page": 100,
                  "text": keyword,
                  "only_with_salary": True,
                  "area": 113,
                  }
        json_response = requests.get(self.url, params).json()['items']
        return json_response

    def get_vacancies(self, keyword):
        pages = 1
        response_list = []
        for page in range(pages):
            print(f"Парсинг страницы {page + 1}", end=": ")
            values = self.get_data(keyword, page)
            print(f"Найдено {len(values)} вакансий")
            response_list.extend(values)
            return response_list


class Currency_API(API_Data):
    """Класс для получения курса валют к рублю"""

    url = "https://api.apilayer.com/exchangerates_data/latest"

    def get_data(self, base: str):
        response = requests.get(self.url, headers={'apikey': API_KEY}, params={'base': base})
        rate = response.json()['rates']['RUB']
        return rate


class SJ_Vacancies_API(API_Data):
    """Класс для получения информации по вакансиям из Superjob"""

    url = 'https://api.superjob.ru/2.0/vacancies'
    sj_api_key = "v3.r.137519672.3bf53585877e7b283aa4e4997571bd7f07e1225e.8d093a7decd52e846d246cf0411b55d35ffefd76"
    headers = {'X-Api-App-Id': sj_api_key}

    def get_data(self, keyword: str, page: int):
        params = {"page": page,
                  "count": 100,
                  "keyword": keyword,
                  "c": 1,
                  }
        json_response = requests.get(self.url, params=params, headers=self.headers).json()['objects']
        return json_response

    def get_vacancies(self, keyword):
        pages = 1
        response_list = []
        for page in range(pages):
            print(f"Парсинг страницы {page + 1}", end=": ")
            values = self.get_data(keyword, page)
            print(f"Найдено {len(values)} вакансий")
            response_list.extend(values)

        return response_list


class Vacancy:

    """Класс для работы с вакансиями"""

    __slots__ = ('id', 'name', 'location', 'salary_min', 'salary_max', 'currency', 'employer', 'link', 'salary_sort_min',
    'salary_sort_max')

    def __init__(self, id, name, location, salary_min, salary_max, currency, employer, link):
        self.id = id
        self.name = name
        self.location = location
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.employer = employer
        self.link = link

        self.salary_sort_min = salary_min
        self.salary_sort_max = salary_max
        if currency and currency not in ['RUR', "rub"]  and (salary_min and salary_max) is not None:
            self.salary_sort_min = self.salary_sort_min * Currency_API().get_data(currency)
            self.salary_sort_max = self.salary_sort_max * Currency_API().get_data(currency)

    def __str__(self):
        salary_min = self.salary_min if self.salary_min is not None else "минимальная зарплата не указана"
        salary_max = self.salary_max if self.salary_max is not None else "максимальная зарплата не указана"
        currency = self.currency if self.currency else ""
        return f"Вакансия: {self.id}: {self.name}\nЛокация: {self.location} \n" \
               f"Зарплата: от {salary_min} до {salary_max} {currency}\n" \
               f"Работодатель: {self.employer}, url: {self.link}"

    def __gt__(self, other):
        if not other.salary_sort_min:
            return True
        if not self.salary_sort_min:
            return False
        return self.salary_sort_min >= other.salary_sort_min


class Json_File(ABC):
    """Абстрактный класс для работы с файлом Json"""

    @abstractmethod
    def add_vacancies(self):
        pass

    @abstractmethod
    def select(self):
        pass


class Json_HH(Json_File):
    """Класс для получения информации из файла .json на НН"""

    def __init__(self, keyword):
        self.__filename = f'{keyword.title()}.json'

    @property
    def filename(self):
        return self.__filename

    def add_vacancies(self, data):
        with open(self.filename, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def select(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []
        for item in data:
            salary_min, salary_max, currency = None, None, None
            if item['salary']:
                salary_min, salary_max, currency = item['salary']['from'], item['salary']['to'], item['salary'][
                    'currency']
            vacancies.append(Vacancy(item['id'], item['name'], item['area']['name'], salary_min,
                                     salary_max, currency, item['employer']['name'],
                                     item['alternate_url']))
        return vacancies


class Json_SJ(Json_HH, Json_File):
    """Класс для получения информации из файла .json на SJ"""

    def select(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        vacancies = []
        for item in data:
            salary_min, salary_max, currency = None, None, None
            if item['payment_from']:
                salary_min, salary_max, currency = item['payment_from'], item['payment_to'], item['currency']
            vacancies.append(Vacancy(item['id'], item['profession'], item['town']['title'], salary_min,
                                     salary_max, currency, item['firm_name'], item['link']))
        return vacancies
