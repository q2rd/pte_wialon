from typing import Optional

from geopy.distance import geodesic

from apis.maps import CityCords, VehicleCords


def check_radius(city: CityCords, vehicle: tuple[float,float], radius: int = 10) -> bool:
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


def find_entry_exit_points(city: CityCords, cords: list[tuple]) -> tuple[
    Optional[tuple[float, float, float]], Optional[tuple[float, float, float]]]:
    """
    Алгоритм для нахождения 2-х точек вхождения в радиус точки координат.
    Возвращает кортежи с первой и последней точкой вхождения в радиус.

    :param city: Pydantic-модель содержащая широту и долготу точек координат города.
    :param cords: Массив кортежей точек координат машины за период.
    :return:
    """
    entry_point = None
    exit_point = None
    in_radius = False
    for cord in cords:
        lat, lon, timestamp = cord
        point_in_radius = check_radius(city, (lat, lon))
        if point_in_radius:
            if not in_radius:
                entry_point = cord
            in_radius = True
            exit_point = cord
        else:
            if in_radius:
                break
            in_radius = False

    return entry_point, exit_point
