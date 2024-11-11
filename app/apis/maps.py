from pydantic import BaseModel


class BaseCords(BaseModel):
    latitude: float
    longitude: float


class CityCords(BaseCords):
    ...

class VehicleCords(BaseCords):
    ...

class ApiResponse(BaseCords):
    total_time: str

class VehiclePath(BaseModel): 
    route: list[VehicleCords]

class RequestPayload(BaseModel):
    load_place: CityCords
    unload_place : CityCords
    plate: str
    time_from: int
    time_to: int
    buffer_time: int


class WialonVehicleResponse(BaseModel):
    id: int # ID машины в Wialon`e.
    nm: str # Гос.номер автомобиля (в wialon`e это поле "name").
