class Vacancy:
    title: str
    link: str
    salary: int
    description: str

    __slots__ = ["title", "link", "salary", "description"]

    def __init__(self, title, link, salary, description):
        self.title = self.__validate_title(title)
        self.link = self.__validate_link(link)
        self.salary = self.__validate_salary(salary)
        self.description = self.__validate_description(description)

    def __validate_title(self, title):
        """Валидация названия вакансии"""
        if not title:
            raise ValueError("Название вакансии не может быть пустым")
        return title

    def __validate_link(self, link):
        """Валидация ссылки на вакансию"""
        if "http" not in link:
            raise ValueError("Ссылка на вакансию должна быть валидным URL.")
        return link

    def __validate_salary(self, salary):
        """Валидация зарплаты. Если зарплата не указана, то возвращается 0"""
        if not salary or salary == "Зарплата не указана":
            return 0
        if isinstance(salary, int):
            return salary
        salary = salary.replace(" ", "").replace("руб.", "")
        if "-" in salary:
            salary = salary.split("-")[0]
        return int(salary)

    def __validate_description(self, description):
        """Валидация описания вакансии"""
        if not description:
            return "Описание отсуствует"
        return description

    def __lt__(self, other):
        """Сравнение вакансий по зарплате"""
        return self.salary < other.salary

    def __repr__(self):
        return f"Vacancy(title={self.title}, salary={self.salary}, link={self.link})"

    def to_dict(self):
        """Преобразует объект Vacancy в словарь."""
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
        }

    @classmethod
    def cast_to_object_list(cls, vacancies_data: list):
        """Преобразует JSON-данные в список объектов Vacancy."""
        vacancies = []
        for item in vacancies_data:
            title = item.get("name")
            link = item.get("alternate_url")
            salary = item.get("salary", {}).get("from") if item.get("salary") else "Зарплата не указана"
            description = item.get("snippet", {}).get("requirement", "")
            vacancies.append(cls(title, link, salary, description))
        return vacancies
