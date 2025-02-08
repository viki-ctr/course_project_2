from src.get_vacancies_api import HeadHunterAPI
from src.save_json import JSONSaver
from src.work_with_vacancies import Vacancy


def user_interaction():
    hh_api = HeadHunterAPI()
    storage = JSONSaver("vacancies.json")

    query = input("Введите поисковый запрос: ")
    vacancies_data = hh_api.get_vacancies(query)

    vacancies = [
        Vacancy(
            item.get("name", "Без названия"),
            item.get("alternate_url", "#"),
            item.get("salary", {}).get("from", 0),
            item.get("snippet", {}).get("requirement", "Описание отсутствует")
        )
        for item in vacancies_data
    ]
    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    top_n = int(input("Введите количество вакансий для вывода: "))
    sorted_vacancies = sorted(vacancies, key=lambda v: v.salary, reverse=True)[:top_n]
    print("Топ вакансий по зарплате:")
    for vacancy in sorted_vacancies:
        print(vacancy)

    keyword = input("Введите ключевое слово для фильтрации: ")
    filtered_vacancies = storage.get_vacancies({"description": keyword})
    print("Отфильтрованные вакансии:")
    for vacancy in filtered_vacancies:
        print(vacancy)




if __name__ == "__main__":
    user_interaction()