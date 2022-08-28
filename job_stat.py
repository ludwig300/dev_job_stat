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
        response_json = response.json()
        vacancies.append(response_json)
        pages_number = response_json['pages']
        page += 1
    return vacancies


def get_vacancies_from_api_sj(language, sj_api_key):
    moscow_id = '4'
    developer_catalog_id = 48
    page = 0
    pages_number = 1
    vacancies = list()
    payload = {
        'keyword': f'Программист {language}',
        'catalogues': developer_catalog_id,
        'town': moscow_id,
        'page': page
    }
    headers = {
        'X-Api-App-Id': sj_api_key
    }
    api_url = 'https://api.superjob.ru/2.0/vacancies/'
    while page < pages_number:
        response = requests.get(api_url, headers=headers, params=payload)
        response.raise_for_status()
        response_json = response.json()
        vacancies.append(response_json)
        page = payload['page']
        if not response_json['more']:
            break
        payload['page'] = page + 1
    return vacancies


def get_average_salaries(vacancies, average_salaries, func):
    for vacancy in vacancies:
        try:
            average_salary = int(func(vacancy))
            average_salaries.append(average_salary)
        except:
            average_salary = None
    return average_salaries


def get_expected_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    elif salary_to:
        return int(salary_to * 0.8)
    elif salary_from:
        return int(salary_from * 1.2)


def predict_rub_salary_hh(vacancy):
    salary_from, salary_to = vacancy['salary']['from'], vacancy['salary']['to']
    currency = vacancy['salary']['currency']
    if 'RUR' in currency:
        average_salary = get_expected_salary(salary_from, salary_to)
    else:
        average_salary = None
    return average_salary


def predict_rub_salary_for_superjob(vacancy):
    salary_from, salary_to = vacancy['payment_from'], vacancy['payment_to']
    currency = vacancy['currency']
    if 'rub' in currency:
        average_salary = get_expected_salary(salary_from, salary_to)
    else:
        average_salary = None
    return average_salary


def get_salary_statistics_sj(languages, sj_api_key):
    salary_statistics = dict()
    average_salaries = list()
    for language in languages:
        sj_vacancies = get_vacancies_from_api_sj(language, sj_api_key)
        value_statistics = dict()
        found_vacancies = dict()
        for vacancies in sj_vacancies:
            found_vacancies[language] = vacancies['total']
            vacancies_average_salaries = get_average_salaries(
                vacancies['objects'],
                average_salaries,
                predict_rub_salary_for_superjob
            )
        value_statistics['vacancies_found'] = found_vacancies[language]
        value_statistics['vacancies_processed'] = len(
            vacancies_average_salaries
        )
        value_statistics['average_salary'] = int(
            mean(
                vacancies_average_salaries
            )
        )
        salary_statistics[language] = value_statistics
    return salary_statistics


def get_salary_statistics_hh(languages):
    salary_statistics = dict()
    average_salaries = list()
    for language in languages:
        hh_vacancies = get_vacancies_from_api_hh(language)
        value_statistics = dict()
        found_vacancies = dict()
        for vacancies in hh_vacancies:
            found_vacancies[language] = vacancies['found']
            vacancies_average_salaries = get_average_salaries(
                vacancies['items'],
                average_salaries,
                predict_rub_salary_hh
            )
        value_statistics['vacancies_found'] = found_vacancies[language]
        value_statistics['vacancies_processed'] = len(
            vacancies_average_salaries
        )
        value_statistics['average_salary'] = int(
            mean(
                vacancies_average_salaries
            )
        )
        salary_statistics[language] = value_statistics
    return salary_statistics


def get_table(table_elements, title):
    table_template = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ],
    ]
    for element in table_elements:
        table_template.append(
            [
                element,
                table_elements[element]['vacancies_found'],
                table_elements[element]['vacancies_processed'],
                table_elements[element]['average_salary']
            ]
        )
    table = AsciiTable(table_template, title)
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
    salary_statistics_hh = get_salary_statistics_hh(languages)
    salary_statistics_sj = get_salary_statistics_sj(languages, sj_api_key)
    print(get_table(salary_statistics_hh, 'HeadHunter Moscow'))
    print(get_table(salary_statistics_sj, 'SuperJob Moscow'))


if __name__ == '__main__':
    main()
