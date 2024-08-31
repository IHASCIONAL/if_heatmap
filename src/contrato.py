from pydantic import BaseModel


class Orders(BaseModel):
    logistic_region: str
    origin_uuid: str
    origin_name: str
    origin_latitude: float
    origin_longitude: float
    Pedidos: int
    shift: str

