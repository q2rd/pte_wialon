import os
from pprint import pprint

import uvicorn
from fastapi import FastAPI, APIRouter

from apis.maps import CityCords

from apis.wialon.core import CustomWialon
from dotenv import load_dotenv
load_dotenv()

from database.sqlite import create_db, insert_vehicles, get_by_plate, init_db
from routs.v1.sub_route import router as r

app = FastAPI(on_startup=init_db())
api_v1 = APIRouter(prefix="/api/v1")
api_v1.include_router(r, prefix="/test")
app.include_router(api_v1)


# if __name__ == '__main__':
    # wia = CustomWialon(token=os.getenv("TOKEN"), host=os.getenv("HOST"))
    # data = wia.get_all_items()
    # create_db()
    # insert_vehicles(data)
    # print(get_by_plate("C480MC193").wialon_id)
    # data = wia.get_vehicle_history(vehicle_id=27557076, time_from=1730458800, time_to=1730471100)
    # # print(data)
    # city = CityCords(**{"latitude": 44.717920377, "longitude": 37.7786819138})
    # first, last = find_entry_exit_points(city=city, cords=data, buffer_time=6700)
    # print(first, last)
    # print(f"машина была в радиусе: {time_formatter(first, last)}")


