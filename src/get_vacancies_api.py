import requests

from src.job_platform import JobPlatformApi


class HeadHunterAPI(JobPlatformApi):
    """Создан класс, который получает данные по API"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__session = requests.Session()

    def __get_vacancies(self, query: str, **kwargs):
        """Получение вакансии по запросу"""
        params = {"text": query, "page": kwargs.get("page", 0), "per_page": kwargs.get("per_page", 100)}
        response = self.__session.get(self.__url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed with status code: {response.status_code}")

    def get_vacancies(self, query: str, **kwargs):
        return self.__get_vacancies(query, **kwargs)


if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python Developer", page=0, per_page=10)
    if vacancies:
        for vacancy in vacancies.get("items", []):
            print(f"Vacancy: {vacancy['name']}, Salary: {vacancy.get('salary', 'Not specified')}")
