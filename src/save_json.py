import json
from src.parent_to_json_saver import Storage
from src.work_with_vacancies import Vacancy


class JSONSaver(Storage):
    """Класс для сохранения вакансий в файл"""
    def __init__(self, filename="vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy: Vacancy):
        """Добавление вакансий"""
        data = self._load_data()
        data.append(vacancy.__dict__)
        self._save_data(data)

    def get_vacancies(self, criteria: dict):
        """Получение вакансий"""
        data = self._load_data()
        return [item for item in data if all(item.get(key) == value for key, value in criteria.items())]

    def delete_vacancy(self, vacancy_id: str):
        """Удаление вакансий"""
        data = self._load_data()
        data = [item for item in data if item.get("link") != vacancy_id]
        self._save_data(data)

    def _load_data(self):
        """Чтение файла (преобразование в объект Python)"""
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_data(self, data):
        """Запись файла (преобразование объекта Python в JSON"""
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
