import os

from apis.maps import CityCords
from apis.utils import find_entry_exit_points
from apis.wialon.core import CustomWialon
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    wia = CustomWialon(token=os.getenv("TOKEN"), host=os.getenv("HOST"))
    data = wia.get_vehicle_history(vehicle_id=27744559, time_from=1730494800, time_to=1730754000)
    # print(data)
    city = CityCords(**{"latitude": 49.6361866667,"longitude":40.5459433333})
    first, last = find_entry_exit_points(city=city, cords=data)
    print(f"машина была в радиусе: {(last[2] - first[2]) / 3600:.2f} часа")
