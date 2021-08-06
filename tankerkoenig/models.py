from pydantic import BaseModel
from typing import List, Any, Union, Dict, Optional
import uuid

Price = Union[float, bool, None]
AddressPart = Union[str, bool, int, None]
# TODO: Move models into files for the different routes
class List_PetrolStation(BaseModel):
    id: uuid.UUID
    name: str
    brand: AddressPart
    lat: float
    lng: float
    dist: float
    price: Price
    diesel: Price
    e5: Price
    e10: Price
    isOpen: Union[bool, str, None]
    houseNumber: AddressPart
    postCode: AddressPart


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
    name: AddressPart
    brand: AddressPart
    street: AddressPart
    houseNumber: AddressPart
    postCode: AddressPart
    place: AddressPart
    openingTimes: List[Details_OpeningTime]
    overrides: List[str]
    wholeDay: Union[bool, str, None]
    isOpen: Union[bool, str, None]
    e5: Price
    e10: Price
    diesel: Price
    lat: float
    lng: float
    state: AddressPart


class Details_Model(BaseModel):
    ok: bool
    license: str
    data: str
    status: str
    station: Details_Station


class Prices_Station(BaseModel):
    status: str
    e5: Price
    e10: Price
    diesel: Price


class Prices_Model(BaseModel):
    ok: bool
    license: str
    data: str
    prices: Dict[str, Prices_Station]
