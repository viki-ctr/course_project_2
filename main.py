from src.get_vacancies_api import HeadHunterAPI
from src.save_json import JSONSaver
from src.work_with_vacancies import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    storage = JSONSaver("vacancies.json")

    query = input("Введите поисковый запрос: ")
    vacancies_data = hh_api.get_vacancies(query)

    vacancies = [Vacancy(item["name"], item["alternate_url"], item["salary"]["from"] if item["salary"] else 0, item["snippet"]["requirement"]) for item in vacancies_data]
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    top_n = int(input("Введите количество вакансий для вывода: "))
    sorted_vacancies = sorted(vacancies, reverse=True)[:top_n]
    print("Топ вакансий по зарплате:")
    for vacancy in sorted_vacancies:
        print(vacancy)

    keyword = input("Введите ключевое слово для фильтрации: ")
    filtered_vacancies = storage.get_vacancies({"description": keyword})
    print("Отфильтрованные вакансии:")
    for vacancy in filtered_vacancies:
        print(vacancy)
