from wialon import Wialon

from apis.maps import WialonVehicleResponse
from apis.wialon.decors import session
from apis.wialon.utils import serialize, read_json


class CustomWialon(Wialon):
    """
    Надстройка над основным классов Wialon`a с набором конкретных методов.
    """
    def __init__(self, host: str, token: str):
        super().__init__(host=host)
        self.token = token

    @session
    def get_all_items(self, item_type: str = "avl_unit", prop_name: str = "sysname") -> list[WialonVehicleResponse]:
        """
        Возвращает список всех объектов (машин по дефолту, кроме тестовых) сериализованных в pydantic-модель.
        Если объект - машина (в моем случае другого не нужно):
            - Содержит полную информацию об устройстве, включая текущее местоположение (в системе координат WGS-84).
            - Информация датчиков, таких как: уровень топлива в баках, кол-во часов работы двигателя и тд.

        :param item_type: Тип объекта, информацию о котором нужно найти.
        :param prop_name: Имя свойства, по которому будет осуществляться поиск.
        :return:
        """
        params = {
            "spec": {
                "itemsType": item_type,
                "propName": prop_name,
                "propValueMask": "*",
                "sortType": prop_name
            },
            "force": 1,
            "flags": 1,
            "from": 0,
            "to": 0
        }
        return serialize(
            self.core_search_items(**params).get("items", "error")
        )

    @session
    def get_sing_item(self, item_id: int, flag: int = 1025):
        """
        Возвращает объект найденный по ID, в моем случае это так же автомобиль.

        :param item_id: ID объекта.
        :param flag: Параметр отвечает за полноту информации в ответе. 1025 - включить координаты в ответ.
        :return:
        """
        params = {
            "id": item_id,
            "flags": flag
        }
        val = self.core_search_item(**params)
        return val

    @session
    def get_vehicle_history(self, vehicle_id: int, time_from: float, time_to: float) -> list[tuple]:
        """
        Получает массив с данными в указанном промежутке времени для автомобиля.
        (В среднем датчик присылает где-то 2 сообщения в минуту.)

        :param vehicle_id: ID автомобиля.
        :param time_from: Промежуток времени "С".
        :param time_to: Промежуток времени "ПО".
        :return:
        """
        params = {
            "itemId": vehicle_id,
            "timeFrom": time_from,
            "timeTo": time_to,
            "flags": 0x0000, # включить все данные в ответ
            "flagsMask": 0xFF00, # по доке не пон что это, но надо так же как выше.
            "loadCount": 10000, # количество сообщений, которое нужно включить в ответ.
        }
        return read_json(self.messages_load_interval(**params).get("messages"))
