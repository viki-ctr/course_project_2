from abc import ABC, abstractmethod


class JobPlatformApi(ABC):
    """Создан базовый абстрактный класс"""
    @classmethod
    @abstractmethod
    def get_vacancies(cls, *args, **kwargs):
        pass