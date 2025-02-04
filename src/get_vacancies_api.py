from src.job_platform import JobPlatformApi
import requests


class HeadHunterAPI(JobPlatformApi):
    """Создан класс, который получает данные по API"""
    def __init__(self):
        self.url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, query: str):
        """Получение вакансии по запросу"""
        pass
