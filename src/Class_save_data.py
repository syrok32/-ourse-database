import psycopg2
from typing import List


class SaveToDB:
    """Сохранение информации в БД"""

    @classmethod
    def save_data_to_database(cls, data: List[dict], database_name: str, params: object) -> None:
        """
        Заполнение созданях твблиуц данными
        :type params: object
        :param data:
        :param database_name:
        :param params:
        :return:
        """

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            for emp in data:
                emp_name_hh = emp["employer_id"]
                cur.execute(
                    """INSERT INTO employers (employers_name, employers_id_hh)
                       VALUES (%s, %s)
                       RETURNING employers_id
                    """,
                    (emp_name_hh["name"], emp_name_hh["id"]),
                )

                employer_id = cur.fetchone()
                if employer_id is None:
                    cur.execute(
                        """
                        SELECT employers_id FROM employers WHERE employers_id_hh = %s
                        """,
                        (emp_name_hh["id"],),
                    )
                    employer_id = cur.fetchone()[0]
                else:
                    employer_id = employer_id[0]

                vacancies_data = emp["vacancies"]
                for vacancy in vacancies_data:
                    salary = None
                    if vacancy.get("salary"):
                        salary = vacancy["salary"].get("from") or vacancy["salary"].get("to")
                    vacancy_employer = vacancy["employer"]
                    cur.execute(
                        """
                        INSERT INTO vacancy(vacancy_title, vacancy_link, vacancy_salary, employers_id)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            vacancy["name"],
                            vacancy_employer["alternate_url"],
                            salary,
                            employer_id,
                        ),
                    )
        conn.commit()
        conn.close()
