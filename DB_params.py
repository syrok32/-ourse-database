import psycopg2
from config import config

params = config()


class DBManager:
    """Выввод из баззы даных"""

    def __init__(self, database_name: str, params):
        """
        Инициализация подключения к базе данных.
        :param database_name:
        :param params:
        """
        self.database_name = database_name
        self.params = params

    def _connect(self):
        return psycopg2.connect(dbname=self.database_name, **self.params)

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """
                SELECT e.employers_name, COUNT(v.vacancy_id) AS vacancies_count
                FROM employers e
                LEFT JOIN vacancy v ON e.employers_id = v.employers_id
                GROUP BY e.employers_name
                ORDER BY vacancies_count DESC;
                """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        :return:
        """
        query = """
            SELECT employers_name, vacancy_title, vacancy_link, vacancy_salary FROM vacancy
            JOIN employers ON vacancy.employers_id= employers.employers_id
            """

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        query = """
                SELECT AVG(vacancy_salary) AS salary_avg FROM vacancy
                """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = """
                SELECT
                vacancy_title,
                vacancy_link,
                vacancy_salary
                FROM
                    vacancy
                WHERE
                vacancy_salary > (SELECT AVG(vacancy_salary) FROM vacancy )

                """
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        query = """
            SELECT * FROM vacancy
            WHERE LOWER(vacancy_title) LIKE LOWER(%s);
               """
        keyword = f"%{keyword}%"

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (keyword,))

                return cur.fetchall()


#
# db_manager = DBManager("Vacansi", params)
# db_manager.get_companies_and_vacancies_count()
# db_manager.get_all_vacancies()
# db_manager.get_avg_salary()
# db_manager.get_vacancies_with_higher_salary()
