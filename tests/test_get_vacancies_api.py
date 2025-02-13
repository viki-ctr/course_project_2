import unittest
from unittest import mock
import requests_mock
from src.get_vacancies_api import HeadHunterAPI
import requests


def test_initialization():
    """Тест инициализации приватных атрибутов."""
    api = HeadHunterAPI()
    mock_url = "https://api.hh.ru/vacancies"

    assert api._HeadHunterAPI__url == mock_url
    assert isinstance(api._HeadHunterAPI__session, requests.Session)


def test_get_vacancies_success():
    """Тест успешного получения вакансий."""
    api = HeadHunterAPI()
    mock_url = "https://api.hh.ru/vacancies"
    mock_query = "Python Developer"
    mock_response = {
        "items": [
            {"id": "1", "name": "Python Developer", "salary": {"from": 100000, "to": 150000}},
            {"id": "2", "name": "Senior Python Developer", "salary": None}
        ]
    }

    with requests_mock.Mocker() as m:
        m.get(mock_url, json=mock_response, status_code=200)
        result = api.get_vacancies(mock_query)
        expected_items = mock_response["items"]

        assert result == expected_items, f"Ожидался ответ {expected_items}, но получен {result}"
        assert len(result) == 2, f"Ожидалось 2 вакансии, но получено {len(result)}"
        first_vacancy = result[0]
        assert first_vacancy["name"] == "Python Developer", "Название первой вакансии не совпадает"
        assert first_vacancy["salary"]["from"] == 100000, "Зарплата первой вакансии не совпадает"


def test_get_vacancies_failure():
    """Тест обработки ошибки при запросе."""
    api = HeadHunterAPI()
    mock_url = "https://api.hh.ru/vacancies"
    mock_query = "Python Developer"

    with requests_mock.Mocker() as m:
        m.get(mock_url, status_code=500)

        try:
            api.get_vacancies(mock_query)
            assert False, "Ожидалось исключение при ошибке API"
        except Exception as e:
            assert "API request failed with status code: 500" in str(e), "Некорректное сообщение об ошибке"


def test_get_vacancies_with_params():
    """Тест с дополнительными параметрами (page и per_page)."""
    api = HeadHunterAPI()
    mock_url = "https://api.hh.ru/vacancies"
    mock_query = "python developer"
    mock_response = {
        "items": [
            {"id": "1", "name": "Python Developer", "salary": {"from": 100000, "to": 150000}},
            {"id": "2", "name": "Senior Python Developer", "salary": None}
        ]
    }

    with requests_mock.Mocker() as m:
        m.get(mock_url, json=mock_response, status_code=200)
        result = api.get_vacancies(mock_query, page=1, per_page=50)
        assert m.last_request.qs["text"][0] == mock_query, "Параметр 'text' должен соответствовать запросу"
        assert m.last_request.qs["page"][0] == "1", "Параметр 'page' должен быть равен 1"
        assert m.last_request.qs["per_page"][0] == "50", "Параметр 'per_page' должен быть равен 50"
