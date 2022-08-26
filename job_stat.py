import requests
import os
from statistics import mean
from terminaltables import AsciiTable
from dotenv import load_dotenv


def get_vacancies_from_api_hh(dev_language):
    page = 0
    pages_number = 1
    vacancies = list()
    moscow_id = '113'
    count_days = '30'
    while page < pages_number:
        payload = {
            'text': f'Developer {dev_language}',
            'area': moscow_id,
            'period': count_days,
            'page': page
        }
        api_url = 'https://api.hh.ru/vacancies'
        response = requests.get(api_url, params=payload)
        response.raise_for_status()
        vacancies.append(response.json())
        pages_number = response.json()['pages']
        page += 1
    return vacancies


def get_average_salaries(vacancies, average_salaries, func):
    for vacancy in vacancies:
        try:
            average_salary = int(func(vacancy))
            average_salaries.append(average_salary)
        except:
            average_salary = None
    return average_salaries


def get_average_salary(average_salaries):
    average_salary = mean(average_salaries)
    return int(average_salary)


def predict_rub_salary_hh(vacancy):
    salary_from, salary_to = vacancy['salary']['from'], vacancy['salary']['to']
    currency = vacancy['salary']['currency']
    if 'RUR' in currency:
        if not salary_from:
            average_salary = salary_to * 0.8
        elif not salary_to:
            average_salary = salary_from * 1.2
        else:
            average_salary = (salary_from + salary_to) // 2
    else:
        average_salary = None
    return average_salary


def predict_rub_salary_for_superJob(vacancy):
    salary_from, salary_to = vacancy['payment_from'], vacancy['payment_to']
    currency = vacancy['currency']
    if 'rub' in currency:
        if salary_from > 0 and salary_to == 0:
            average_salary = salary_from * 1.2
        elif salary_to > 0 and salary_from == 0:
            average_salary = salary_to * 0.8
        elif salary_to == 0 and salary_from == 0:
            average_salary = None
        else:
            average_salary = (salary_from + salary_to) // 2
    else:
        average_salary = None
    return average_salary


def get_vacancies_from_api_sj(language, sj_api_key):
    moscow_id = '4'
    developer_catalog_id = 48
    count_vacancies = 100
    payload = {
        'keyword': f'Программист {language}',
        'catalogues': developer_catalog_id,
        'town': moscow_id,
        'count': count_vacancies,
    }
    headers = {
        'X-Api-App-Id': sj_api_key
    }
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    response = requests.get(api_url, headers=headers, params=payload)
    response.raise_for_status()
    vacancies = response.json()
    return vacancies


def get_salary_statistics_hh(languages):
    salary_statistics = dict()
    average_salaries = list()
    for language in languages:
        vacancies_hh = get_vacancies_from_api_hh(language)
        value_statistics = dict()
        vacancies_found = dict()
        for vacancies in vacancies_hh:
            vacancies_found[language] = vacancies['found']
            average_salaries_vacancies = get_average_salaries(
                vacancies['items'],
                average_salaries,
                predict_rub_salary_hh
            )
        value_statistics['vacancies_found'] = vacancies_found[language]
        value_statistics['vacancies_processed'] = len(average_salaries_vacancies)
        value_statistics['average_salary'] = get_average_salary(
            average_salaries_vacancies
        )
        salary_statistics[language] = value_statistics
    return salary_statistics


def get_salary_statistics_sj(languages, sj_api_key):
    salary_statistics = dict()
    average_salaries = list()
    for language in languages:
        vacancies_sj = get_vacancies_from_api_sj(language, sj_api_key)
        value_statistics = dict()
        vacancies_found = dict()
        vacancies_found[language] = vacancies_sj['total']
        average_salaries_vacancies = get_average_salaries(
            vacancies_sj['objects'],
            average_salaries,
            predict_rub_salary_for_superJob
        )
        value_statistics['vacancies_found'] = vacancies_found[language]
        value_statistics['vacancies_processed'] = len(average_salaries_vacancies)
        value_statistics['average_salary'] = get_average_salary(
            average_salaries_vacancies
        )
        salary_statistics[language] = value_statistics
    return salary_statistics


def get_table(database, title):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    for element in database:
        table_data.append(
            [
                element,
                database[element]['vacancies_found'],
                database[element]['vacancies_processed'],
                database[element]['average_salary']
            ]
        )
    table = AsciiTable(table_data, title)
    return table.table


def main():
    load_dotenv()
    sj_api_key = os.environ['SJ_API_KEY']
    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C'
    ]
    database_hh = get_salary_statistics_hh(languages)
    database_sj = get_salary_statistics_sj(languages, sj_api_key)
    print(get_table(database_hh, 'HeadHunter Moscow'))
    print(get_table(database_sj, 'SuperJob Moscow'))


if __name__ == '__main__':
    main()
