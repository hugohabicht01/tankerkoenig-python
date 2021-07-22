from pydantic import BaseModel
from typing import List
from enum import Enum
import uuid


class PetrolStation(BaseModel):
    id: uuid.UUID
    name: str
    brand: str
    lat: float
    lng: float
    dist: float
    price: float
    isOpen: bool = None
    houseNumber: str = None
    postCode: int = None

class PetrolStations(BaseModel):
    ok: bool
    license: str
    data: str
    status: str
    stations: List[PetrolStation] = None

class Petrol(Enum):
    DIESEL = 'diesel'
    E5 = 'e5'
    E10 = 'e10'
    ALL = 'all'

class SortingMethod(Enum):
    DISTANCE = 'dist'
    PRICE = 'price'