import unittest
from unittest.mock import mock_open, patch
import json
from src.save_json import JSONSaver, Vacancy


class TestJSONSaver(unittest.TestCase):
    def setUp(self):
        """Настройка перед каждым тестом."""
        self.filename = "test_vacancies.json"
        self.saver = JSONSaver(self.filename)
        self.vacancy1 = Vacancy("Python Developer", "http://example.com/1",
                                "100000-150000", "Описание 1")
        self.vacancy2 = Vacancy("Java Developer", "http://example.com/2",
                                "120000-160000", "Описание 2")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_add_vacancy(self, mock_file):
        """Тест добавления вакансии."""
        self.saver.add_vacancy(self.vacancy1)

        # Проверяем, что файл был открыт для чтения и записи
        mock_file.assert_any_call(self.filename, "r", encoding="utf-8")  # Чтение
        mock_file.assert_any_call(self.filename, "w", encoding="utf-8")  # Запись

        # Проверяем, что данные были записаны корректно
        written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
        expected_data = json.dumps([self.vacancy1.to_dict()], indent=4)
        self.assertEqual(written_data, expected_data, "Записанные данные не совпадают с ожидаемыми")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"title": "Python Developer", "link": "http://example.com/1"},
        {"title": "Java Developer", "link": "http://example.com/2"}
    ]))
    def test_get_vacancies(self, mock_file):
        """Тест получения вакансий по критериям."""
        criteria = {"title": "python"}  # Критерий фильтрации (регистронезависимый)
        result = self.saver.get_vacancies(criteria)

        # Проверяем, что файл был открыт для чтения
        mock_file.assert_called_once_with(self.filename, "r", encoding="utf-8")

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(len(result), 1, "Ожидалась 1 вакансия")
        self.assertEqual(result[0]["title"], "Python Developer", "Название вакансии не совпадает")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"title": "Python Developer", "link": "http://example.com/1"},
        {"title": "Java Developer", "link": "http://example.com/2"}
    ]))
    def test_delete_vacancy(self, mock_file):
        """Тест удаления вакансии."""
        self.saver.delete_vacancy("http://example.com/1")

        # Проверяем, что файл был открыт для чтения и записи
        mock_file.assert_any_call(self.filename, "r", encoding="utf-8")  # Чтение
        mock_file.assert_any_call(self.filename, "w", encoding="utf-8")  # Запись

        # Проверяем, что данные были записаны корректно
        written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
        expected_data = json.dumps([{"title": "Java Developer", "link": "http://example.com/2"}], indent=4)
        self.assertEqual(written_data, expected_data, "Записанные данные не совпадают с ожидаемыми")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_load_data_empty_file(self, mock_file):
        """Тест загрузки данных из пустого файла."""
        result = self.saver._load_data()

        # Проверяем, что файл был открыт для чтения
        mock_file.assert_called_once_with(self.filename, "r", encoding="utf-8")

        # Проверяем, что результат пуст
        self.assertEqual(result, [], "Ожидался пустой список")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"title": "Python Developer", "link": "http://example.com/1"}
    ]))
    def test_load_data_non_empty_file(self, mock_file):
        """Тест загрузки данных из непустого файла."""
        result = self.saver._load_data()

        # Проверяем, что файл был открыт для чтения
        mock_file.assert_called_once_with(self.filename, "r", encoding="utf-8")

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(len(result), 1, "Ожидалась 1 вакансия")
        self.assertEqual(result[0]["title"], "Python Developer", "Название вакансии не совпадает")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_data(self, mock_file):
        """Тест сохранения данных в файл."""
        data = [{"title": "Python Developer", "link": "http://example.com/1"}]
        self.saver._save_data(data)

        # Проверяем, что файл был открыт для записи
        mock_file.assert_called_once_with(self.filename, "w", encoding="utf-8")

        # Проверяем, что данные были записаны корректно
        written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
        expected_data = json.dumps(data, indent=4)
        self.assertEqual(written_data, expected_data, "Записанные данные не совпадают с ожидаемыми")