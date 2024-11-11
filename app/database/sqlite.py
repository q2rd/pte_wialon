import os
from sqlite3 import connect, Connection, IntegrityError

from apis.maps import WialonVehicleResponse
from apis.wialon.core import CustomWialon
from database.maps import VehicleDBResponse

def get_connection() -> Connection:
    return connect("pte.db")


def create_db():
    with get_connection() as con:
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vehicle (
                id INTEGER PRIMARY KEY,
                plate TEXT UNIQUE,
                wialon_id INTEGER    
            )
            """
        )


def get_by_plate(plate: str) -> VehicleDBResponse | None:
    with get_connection() as con:
        cur = con.cursor()
        res = cur.execute(
            """
            SELECT wialon_id 
            FROM vehicle 
            WHERE plate = ?
            """,
            (plate,)
        ).fetchone()

        if res:
            return VehicleDBResponse(wialon_id=res[0])
        else:
            return None


def insert_vehicles(vehicles: list[WialonVehicleResponse]):
    with get_connection() as con:
        cur = con.cursor()

        for vehicle in vehicles:
            try:
                cur.execute(
                    """
                    INSERT INTO vehicle (plate, wialon_id)
                    VALUES (?, ?)
                    """,
                    (vehicle.nm, vehicle.id)
                )
            except IntegrityError:
                print(f"Запись с plate='{vehicle.nm}' существует.")

        con.commit()


def init_db():
    wia = CustomWialon(token=os.getenv("TOKEN"), host=os.getenv("HOST"))
    create_db()
    insert_vehicles(wia.get_all_items())


def update_db(plate: str) -> str:
    wia = CustomWialon(token=os.getenv("TOKEN"), host=os.getenv("HOST"))
    insert_vehicles(wia.get_all_items())
    with get_connection() as con:
        cur = con.cursor()
        res = cur.execute(
            """
            SELECT wialon_id 
            FROM vehicle 
            WHERE plate = ?
            """,
            (plate,)
        ).fetchone()
        if res is None:
            return "Похоже,такой машины в Wialon нет ://"


