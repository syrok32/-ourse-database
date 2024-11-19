import json
import requests
from Class_abstract import GetApiHH
from Class_employers import Employers


class ApiHH(GetApiHH):
    """
    Класс для взаимодействия с API HeadHunter.
    Позволяет получить JSON-ответ на основе ключевого слова и количества вакансий.
    """

    def __init__(self, count_vac: object) -> None:
        self.count_vac = count_vac
        self.response = self._fetch_data()
        self.employers = Employers.get_data_employers(self.count_vac)

    def _fetch_data(self) -> requests.Response:
        """
        Выполняет запрос к API и возвращает ответ.

        :return: Ответ API в формате requests.Response.
        :raises ValueError: Если статус-код ответа не равен 200.

        """
        employers_list = set(map(lambda x: x["id"], Employers.get_data_employers(self.count_vac)))
        url = "https://api.hh.ru/vacancies"
        params = {"employer_id": employers_list}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise ValueError(f"Ошибка запроса. Статус-код: {response.status_code}")

        return response

    def format_json(self):
        data = self._fetch_data()
        format_data = []

        data_json = data.json()
        for emploer_id in self.employers:
            employe_vacancies = {"employer_id": emploer_id, "vacancies": []}

            for el in data_json["items"]:
                if emploer_id["id"] == el["employer"]["id"]:
                    employe_vacancies["vacancies"].append(el)
            format_data.append(employe_vacancies)

        return format_data

    def save_response_to_file(self, file_path: str = "json_vacancy.json") -> None:
        """
        Сохраняет JSON-ответ в файл.

        :param file_path: Путь к файлу для сохранения данных.
        """
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.format_json(), file, indent=4, ensure_ascii=False)


# name1 = ApiHH()
# name1.save_response_to_file()
