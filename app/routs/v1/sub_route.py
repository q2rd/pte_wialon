from fastapi import APIRouter, Depends

from apis.maps import RequestPayload
from apis.wialon.core import CustomWialon
from apis.wialon.utils import find_entry_exit_points, time_formatter
from database.sqlite import get_by_plate, update_db
from routs.v1.utils import get_wialon

router = APIRouter()




@router.post("/calculate")
def calculate_time(
        payload: RequestPayload,
        wialon: CustomWialon = Depends(get_wialon)

):
    vehicle_id = get_by_plate(payload.plate.upper()).wialon_id
    if vehicle_id is None:
        res = update_db(payload.plate)
        if res:
            return {"err": res}
        vehicle_id = get_by_plate(payload.plate.upper()).wialon_id

    data = wialon.get_vehicle_history(vehicle_id=vehicle_id, time_from=payload.time_from, time_to=payload.time_to)
    first1, last1 = find_entry_exit_points(city=payload.load_place, cords=data)
    first2, last2 = find_entry_exit_points(city=payload.unload_place, cords=data)
    return {
        "load_place": {
            "enter": {
                "lat": first1[0],
                "long": first1[1],
                "time": first1[2]
            },
            "load_place_exit": {
                "lat": last1[0],
                "long": last1[1],
                "time": last1[2]
            },
            "total_time_in_zone": f"{time_formatter(first1, last1)}",
        },
        "unload_place": {
            "enter": {
                "lat": first2[0],
                "long": first2[1],
                "time": first2[2]
            },
            "exit": {
                "lat": last2[0],
                "long": last2[1],
                "time": last2[2]
            },
            "total_time_in_zone": f"{time_formatter(first2, last2)}",
        }
    }
