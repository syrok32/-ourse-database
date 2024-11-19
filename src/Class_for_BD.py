import psycopg2
from psycopg2 import sql


class Database:
    """Создание баззы данных :)"""

    def __init__(self, data_name, params):
        self.data_name = data_name
        self.params = params

    def create_table(self):
        """
        Создание базы данных
        :return:
        """

        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier(self.data_name)))
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self.data_name)))
        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.data_name, **self.params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers(
                    employers_id SERIAL PRIMARY KEY,
                    employers_name VARCHAR(225) NOT NULL,
                    employers_id_hh VARCHAR(225) NOT NULL
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE vacancy(
                    vacancy_id SERIAL PRIMARY KEY,
                    vacancy_title VARCHAR(225) NOT NULL,
                    vacancy_link VARCHAR(225) NOT NULL,
                    vacancy_salary INTEGER,
                    employers_id INTEGER REFERENCES employers(employers_id)
                )
            """
            )

        conn.commit()
        conn.close()


# params = config()
# emp_1 = Database('Vacansi', params)
# emp_1.create_table()
