from Class_for_BD import Database
from Class_save_data import SaveToDB
from Api_HH import ApiHH
from config import config
from DB_params import DBManager


def main():
    count_vac = int(input("Ведите колтчество работодателй: "))

    name1 = ApiHH(count_vac)
    data = name1.format_json()
    params = config()

    name_database = input("Ведите название базы данных: ")
    emp_1 = Database(name_database, params)
    emp_1.create_table()

    SaveToDB.save_data_to_database(data, name_database, params)

    db_manager = DBManager(name_database, params)

    # Меню для взаимодействия с пользователем
    while True:
        print("\nМеню:")
        print("1. Показать список компаний и количество вакансий")
        print("2. Показать все вакансии (название, зарплата, ссылка)")
        print("3. Показать среднюю зарплату")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Найти вакансии по ключевому слову")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()

            for company, count in companies:
                print(f"Компания: {company}, Вакансий: {count}")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            print(vacancies)

            for company, title, link, salary in vacancies:
                print(f"Компания: {company}, Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {round(avg_salary)}")

        elif choice == "4":
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            for title, link, salary in higher_salary_vacancies:
                print(f"Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for ps, title, link, salary, id in vacancies:
                print(f"Вакансия: {title}, Зарплата: {salary}, Ссылка: {link}")

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
