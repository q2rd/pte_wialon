from pydantic import BaseModel


class VehicleDBResponse(BaseModel):
    wialon_id: int
