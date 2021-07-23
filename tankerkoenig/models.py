from pydantic import BaseModel
from typing import List, Any, Union
from enum import Enum
import uuid

# TODO: Move models into files for the different routes
class List_PetrolStation(BaseModel):
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


class List_PetrolStations(BaseModel):
    ok: bool
    license: str
    data: str
    status: str
    stations: List[List_PetrolStation] = None


class Details_OpeningTime(BaseModel):
    text: str
    start: str
    end: str


class Details_Station(BaseModel):
    id: str
    name: str
    brand: str
    street: str
    houseNumber: str
    postCode: int
    place: str
    openingTimes: List[Details_OpeningTime]
    overrides: List[str]
    wholeDay: bool
    isOpen: bool
    e5: float
    e10: float
    diesel: float
    lat: float
    lng: float
    state: Any


class Details_Model(BaseModel):
    ok: bool
    license: str
    data: str
    status: str
    station: Details_Station


class Prices_Station(BaseModel):
    status: str
    e5: Union[float, bool, None]
    e10: Union[float, bool, None]
    diesel: Union[float, bool, None]


class Prices_Model(BaseModel):
    ok: bool
    license: str
    data: str
    prices: List[Prices_Station]


class Petrol(Enum):
    DIESEL = "diesel"
    E5 = "e5"
    E10 = "e10"
    ALL = "all"


class SortingMethod(Enum):
    DISTANCE = "dist"
    PRICE = "price"
