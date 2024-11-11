import os
from typing import Optional

from geopy.distance import geodesic

from apis.maps import CityCords, WialonVehicleResponse


def check_radius(city: CityCords, vehicle: tuple[float,float], radius: int = 13) -> bool:
    """
    Функция проверят, находится ли точка координат в радиусе города.

    :param city:
    :param vehicle:
    :param radius:
    :return:
    """
    distance_km = geodesic((city.latitude, city.longitude), (vehicle[0], vehicle[1])).km
    if distance_km <= radius:
        # print("Машина находится в радиусе 10 км от города.")
        return True
    else:
        # print("Машина за пределами радиуса.")
        return False

def find_entry_exit_points(city: CityCords, cords: list[tuple], buffer_time: int = 3600) -> tuple[
    Optional[tuple[float, float, float]], Optional[tuple[float, float, float]]]:
    """
    Алгоритм для нахождения 2-х точек вхождения в радиус точки координат.
    Учитывает временные выбросы (из-за РЭБ`a).
    Возвращает кортежи с первой и последней точкой вхождения в радиус.

    :param city: Pydantic-модель содержащая широту и долготу точек координат города.
    :param cords: Массив кортежей точек координат машины за период.
    :param buffer_time: Максимальный промежуток времени (в секундах) для игнорирования выбросов.
    :return:
    """
    entry_point = None
    exit_point = None
    in_radius = False
    bad_exit_point = None
    for cord in cords:
        lat, lon, timestamp = cord
        point_in_radius = check_radius(city, (lat, lon))

        if point_in_radius:
            if not in_radius:
                entry_point = cord
            in_radius = True
            exit_point = cord
            bad_exit_point = None
        else:
            if in_radius:
                if bad_exit_point is None:
                    bad_exit_point = cord
                else:
                    if timestamp - bad_exit_point[2] > buffer_time:
                        exit_point = bad_exit_point
                        in_radius = False
                        break
            else:
                bad_exit_point = None

    return entry_point, exit_point



def time_formatter(first: tuple, last:tuple) -> str:
    """
    Форматирует тип "unix timestemp" в человеко читаемый формат.
    :param first:
    :param last:
    :return:
    """
    total_seconds = last[2] - first[2]

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours}ч:{minutes}м:{seconds}с"


# Не нужно, но пусть будет.
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