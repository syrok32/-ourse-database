import requests


class Employers:
    """
    Получение id работодателя
    """

    @classmethod
    def get_data_employers(cls, count_employers):
        """
        Обращение по API
        :param count_employers:
        :return:
        """
        url = "https://api.hh.ru/employers"
        params = {"only_with_vacancies": True, "per_page": count_employers}
        response = requests.get(url, params=params)
        response_dict = response.json()
        return Employers._list_date_name(response_dict)

    @classmethod
    def _list_date_name(self, data):
        """
        Формирование словоря с информцией
        :param data:
        :return: name
        """
        data_dict = data["items"]
        name = []
        for i in data_dict:
            name.append({"id": i["id"], "name": i["name"]})
        return name


#
# print(Employers.get_data_employers(10))
