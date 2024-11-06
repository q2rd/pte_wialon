from pydantic import BaseModel


class BaseCords(BaseModel):
    latitude: float
    longitude: float


class CityCords(BaseCords):
    ...

class VehicleCords(BaseCords):
    ...

class VehiclePath(BaseModel):
    route: list[VehicleCords]


class WialonVehicleResponse(BaseModel):
    id: int # ID машины в Wialon`e.
    nm: str # Гос.номер автомобиля (в wialon`e это поле "name").
