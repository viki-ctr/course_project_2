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
            data = response.json()
            if isinstance(data, dict) and "items" in data:
                return data["items"]
            else:
                raise ValueError("Ответ от API не содержит ключ 'items'")
        else:
            raise Exception(f"API request failed with status code: {response.status_code}")

    def get_vacancies(self, query: str, **kwargs):
        return self.__get_vacancies(query, **kwargs)
