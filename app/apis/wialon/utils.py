import os

from apis.maps import WialonVehicleResponse

# не нужно но пусть будет.
def serialize(data: list[dict[str,str]]) -> list[WialonVehicleResponse]:
    """
    Возвращает массив с сериализованный python-объектами.
    :param data:
    :return:
    """
    serialized_dta = []
    for i in data:
        if i.get("nm") != os.getenv("BAD_VEHICLE"): # тестовый автомобиль.
            serialized_dta.append(WialonVehicleResponse(**i))
    return serialized_dta


def read_json(data: list[dict]) -> list[tuple]:
    """
    Возвращает массив с данными: широта, долгота, временная метка.
    (В среднем датчик присылает где-то 2 сообщения в минуту.)

    :param data:
    :return:
    """
    serialized_data = []
    for row in data:
        serialized_data.append((row.get("pos").get("y"), row.get("pos").get("x"), row.get("t")))
    return serialized_data