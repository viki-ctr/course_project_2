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
    @patch("json.dump")
    def test_add_vacancy(self, mock_json_dump, mock_file):
        """Тест добавления вакансии."""
        self.saver.add_vacancy(self.vacancy1)

        mock_file.assert_any_call(self.filename, "r")
        mock_file.assert_any_call(self.filename, "w")

        expected_data = [self.vacancy1.to_dict()]
        mock_json_dump.assert_called_once_with(expected_data, mock_file(), indent=4)


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"title": "Python Developer",
                                                                           "link": "http://example.com/1"}]))
    def test_get_vacancies(self, mock_file):
        """Тест получения вакансий по критериям."""
        criteria = {"title": "Python Developer"}
        result = self.saver.get_vacancies(criteria)

        mock_file.assert_called_once_with(self.filename, "r")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Python Developer")


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"title": "Python Developer",
                                                                           "link": "http://example.com/1"}]))
    def test_delete_vacancy(self, mock_file):
        """Тест удаления вакансии."""
        self.saver.delete_vacancy("http://example.com/1")

        mock_file.assert_any_call(self.filename, "r")
        mock_file.assert_any_call(self.filename, "w")

        mock_file().write.assert_called_once_with(json.dumps([], indent=4))


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([]))
    def test_load_data_empty_file(self, mock_file):
        """Тест загрузки данных из пустого файла."""
        result = self.saver._load_data()

        mock_file.assert_called_once_with(self.filename, "r")

        self.assertEqual(result, [])


    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"title": "Python Developer",
                                                                     "link": "http://example.com/1"}]))
    def test_load_data_non_empty_file(self, mock_file):
        """Тест загрузки данных из непустого файла."""
        result = self.saver._load_data()

        mock_file.assert_called_once_with(self.filename, "r")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Python Developer")


    @patch("builtins.open", new_callable=mock_open)
    def test_save_data(self, mock_file):
        """Тест сохранения данных в файл."""
        data = [{"title": "Python Developer", "link": "http://example.com/1"}]
        self.saver._save_data(data)

        mock_file.assert_called_once_with(self.filename, "w")

        written_data = "".join(call.args[0] for call in mock_file().write.call_args_list)
        expected_data = json.dumps(data, indent=4)

        self.assertEqual(written_data, expected_data, "Записанные данные не совпадают с ожидаемыми")