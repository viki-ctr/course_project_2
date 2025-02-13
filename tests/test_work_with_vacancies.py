from src.work_with_vacancies import Vacancy
import unittest


def test_valid_initialization():
    """Тест корректной инициализации объекта."""
    vacancy = Vacancy(
        title="Python Developer",
        link="http://example.com",
        salary="100000-150000 руб.",
        description="Описание вакансии"
    )

    assert vacancy.title == "Python Developer", "Название вакансии не совпадает"
    assert vacancy.link == "http://example.com", "Ссылка на вакансию не совпадает"
    assert vacancy.salary == 100000, "Зарплата не совпадает"
    assert vacancy.description == "Описание вакансии", "Описание вакансии не совпадает"


def test_invalid_title():
    """Тест валидации названия вакансии."""
    try:
        Vacancy(title="", link="http://example.com", salary="100000", description="Описание")
        assert False, "Ожидалось исключение ValueError"
    except ValueError as e:
        assert str(e) == "Название вакансии не может быть пустым", "Некорректное сообщение об ошибке"


def test_invalid_link():
    """Тест валидации ссылки на вакансию."""
    try:
        Vacancy(title="Python Developer", link="example.com", salary="100000", description="Описание")
        assert False, "Ожидалось исключение ValueError"
    except ValueError as e:
        assert str(e) == "Ссылка на вакансию должна быть валидным URL.", "Некорректное сообщение об ошибке"


def test_salary_validation():
    """Тест валидации зарплаты."""
    vacancy = Vacancy(title="Python Developer", link="http://example.com", salary="Зарплата не указана", description="Описание")
    assert vacancy.salary == 0, "Зарплата должна быть 0, если не указана"

    vacancy = Vacancy(title="Python Developer", link="http://example.com", salary="100000-150000 руб.", description="Описание")
    assert vacancy.salary == 100000, "Зарплата должна быть 100000"

    vacancy = Vacancy(title="Python Developer", link="http://example.com", salary="120000 руб.", description="Описание")
    assert vacancy.salary == 120000, "Зарплата должна быть 120000"


def test_description_validation():
    """Тест валидации описания вакансии."""

    vacancy = Vacancy(title="Python Developer", link="http://example.com", salary="100000", description="")
    assert vacancy.description == "Описание отсуствует", "Описание должно быть 'Описание отсуствует'"


    vacancy = Vacancy(title="Python Developer", link="http://example.com", salary="100000", description="Описание вакансии")
    assert vacancy.description == "Описание вакансии", "Описание должно совпадать"


def test_lt_comparison():
    """Тест сравнения вакансий по зарплате."""
    vacancy1 = Vacancy(title="Python Developer", link="http://example.com", salary="100000", description="Описание")
    vacancy2 = Vacancy(title="Java Developer", link="http://example.com", salary="120000", description="Описание")

    assert vacancy1 < vacancy2, "Вакансия 1 должна быть меньше вакансии 2 по зарплате"
    assert not (vacancy2 < vacancy1), "Вакансия 2 не должна быть меньше вакансии 1 по зарплате"


class TestVacancy(unittest.TestCase):
    def test_cast_to_object_list(self):
        """Тест преобразования JSON-данных в список объектов Vacancy."""
        vacancies_data = [
            {
                "name": "Python Developer",
                "alternate_url": "http://example.com/1",
                "salary": {"from": 100000},
                "snippet": {"requirement": "Описание 1"}
            },
            {
                "name": "Java Developer",
                "alternate_url": "http://example.com/2",
                "salary": None,
                "snippet": {"requirement": ""}
            }
        ]

        vacancies = Vacancy.cast_to_object_list(vacancies_data)
        self.assertEqual(len(vacancies), 2, "Должно быть 2 вакансии")

    # Проверка первой вакансии
        self.assertEqual(vacancies[0].title, "Python Developer", "Название первой вакансии не совпадает")
        self.assertEqual(vacancies[0].link, "http://example.com/1", "Ссылка первой вакансии не совпадает")
        self.assertEqual(vacancies[0].salary, 100000, "Зарплата первой вакансии не совпадает")
        self.assertEqual(vacancies[0].description, "Описание 1", "Описание первой вакансии не совпадает")

    # Проверка второй вакансии
        self.assertEqual(vacancies[1].title, "Java Developer", "Название второй вакансии не совпадает")
        self.assertEqual(vacancies[1].link, "http://example.com/2", "Ссылка второй вакансии не совпадает")
        self.assertEqual(vacancies[1].salary, 0, "Зарплата второй вакансии должна быть 0")
        self.assertEqual(vacancies[1].description, "Описание отсуствует", "Описание второй вакансии не совпадает")


def test_slots():
    """Тест ограничения атрибутов слотами."""
    vacancy = Vacancy(
        title="Python Developer",
        link="http://example.com",
        salary="100000-150000 руб.",
        description="Описание вакансии"
    )

    try:
        vacancy.invalid_attribute = "test"
        assert False, "Ожидалось исключение AttributeError"
    except AttributeError:
        pass