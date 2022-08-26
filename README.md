# dev_job_stat

## This is a program for collecting statistics on developer vacancies from https://api.hh.ru and https://api.superjob.ru. Developer languages:
- 'JavaScript',
- 'Java',
- 'Python',
- 'Ruby',
- 'PHP',
- 'C++',
- 'C#',
- 'C'

## Installing required dependencies
[Register your application](https://api.superjob.ru/register/). You need `Secret key` look like this `	v3.r.136923447.6b28231684c2802580d391c65d5d57b517830875.849abbcc96c99642d85240f08b9a1762ada30a8e`

## Setting environment variables
* Create `.env` file in project directory and write:
```
SJ_API_KEY = Your Secret key
```		

### Requirements
* python-dotenv==0.20.0
* requests==2.28.1
* terminaltables==3.1.10

Remember, it is recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for better isolation.
Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```		

## Application launch

### Open project directory from cmd
``` 
$ python job_stat.py
```

The cmd will display two tables with results like this:
```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 7439             | 965                 | 152290           |
| Java                  | 5386             | 1421                | 166249           |
| Python                | 7347             | 2052                | 173059           |
| Ruby                  | 365              | 2147                | 172730           |
| PHP                   | 3633             | 3272                | 161820           |
| C++                   | 3460             | 3967                | 158600           |
| C#                    | 3152             | 4646                | 155888           |
| C                     | 12212            | 5530                | 156843           |
+-----------------------+------------------+---------------------+------------------+
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| JavaScript            | 37               | 22                  | 136840           |
| Java                  | 7                | 25                  | 149380           |
| Python                | 27               | 44                  | 153954           |
| Ruby                  | 4                | 46                  | 158760           |
| PHP                   | 20               | 61                  | 155924           |
| C++                   | 17               | 70                  | 154606           |
| C#                    | 7                | 75                  | 158698           |
| C                     | 17               | 87                  | 157050           |
+-----------------------+------------------+---------------------+------------------+
```

## Project Goals
*The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).*
