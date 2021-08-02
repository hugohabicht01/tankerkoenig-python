from typing import List
import requests
from . import models
from . import exceptions
from enum import Enum


class Petrol(Enum):
    DIESEL = "diesel"
    E5 = "e5"
    E10 = "e10"
    ALL = "all"


class SortingMethod(Enum):
    DISTANCE = "dist"
    PRICE = "price"


class Client:
    def __init__(
        self,
        api_key: str = None,
        base_url: str = "https://creativecommons.tankerkoenig.de/json",
    ):
        if api_key is None:
            raise exceptions.invalid_api_key
        self.api_key = api_key
        self.BASE_URL = base_url

    def list(
        self,
        *,
        lat: float,
        lng: float,
        rad: float,
        petrol_type: Petrol,
        sort: SortingMethod,
    ) -> models.List_PetrolStations:
        """
        Fetches all petrol stations in a certain radius from a position and returns their prices

        Args:
            lat (float): Latitude
            lng (float): Longitude
            rad (float): Search radius
            petrol_type (Petrol): Petrol enum
            sort (SortingMethod): Sorting enum

        Returns:
          models.PetrolStations: Object with all the petrol stations in the surroundings

        Raises:
            exceptions.api_error: Unspecified error returned from the tankerkoenig API
            exceptions.invalid_api_key: Bad API key
            exceptions.bad_latitude: Latitude out of bounds or wrong format
            exceptions.bad_longitude: Longitude out of bounds or wrong format
            exceptions.bad_radius: Invalid radius
            requests.exceptions.RequestException: Request error
        """
        url = f"{self.BASE_URL}/list.php"
        r = requests.get(
            url,
            params={
                "lat": lat,
                "lng": lng,
                "rad": rad,
                "sort": sort.value,
                "type": petrol_type.value,
                "apikey": self.api_key,
            },
            timeout=3,
        )
        if r.status_code != 200:
            raise exceptions.api_error(f"HTTP status code: {r.status_code}")
        prices: dict = r.json()

        if prices["ok"] is not True or prices["status"] != "ok":
            msg = prices["message"]
            if msg == "apikey nicht angegeben, falsch, oder im falschen Format":
                raise exceptions.invalid_api_key
            if msg == "lat nicht angegeben, oder ausserhalb der gültigen Grenzen":
                raise exceptions.bad_latitude
            if msg == "lng nicht angegeben, oder ausserhalb der gültigen Grenzen":
                raise exceptions.bad_longitude
            if msg == "rad nicht angegeben, oder ausserhalb des gültigen Bereichs":
                raise exceptions.bad_radius
            raise exceptions.api_error(msg)

        prices_model = models.List_PetrolStations(**prices)

        return prices_model

    def details(self, *, id: str) -> models.Details_Model:
        """
        Fetches details about a petrol station with a given id

        Args:
            id (str): ID of a petrol station

        Returns:
            models.Details_Model: Details of the petrol station

        Raises:
            exceptions.api_error: Unspecified error returned from the tankerkoenig API
            exceptions.invalid_api_key: Bad API key
            exceptions.bad_id: Invalid ID
            requests.exceptions.RequestException: Request error
        """
        url = f"{self.BASE_URL}/detail.php"
        r = requests.get(url, params={"id": id, "apikey": self.api_key}, timeout=3)
        if r.status_code != 200:
            raise exceptions.api_error(f"HTTP status code: {r.status_code}")

        details: dict = r.json()

        if details["ok"] is not True or details["status"] != "ok":
            msg = details["message"]
            if (
                msg == "apikey nicht angegeben, falsch, oder im falschen Format"
                or msg[:38] == "ERROR:  invalid input syntax for uuid:"
            ):
                raise exceptions.invalid_api_key
            if msg == "parameter error":
                raise exceptions.bad_id
            raise exceptions.api_error(msg)

        details_model = models.Details_Model(**details)

        return details_model

    def prices(self, *, ids: List[str]) -> models.Prices_Model:
        """
        Fetches current prices of up to ten petrol stations by IDs

        Args:
            ids (List[str]): List of IDs of petrol stations

        Returns:
            models.Prices_Model: Current prices of all stations

        Raises:
            exceptions.api_error: Unspecified error returned from the tankerkoenig API
            exceptions.invalid_api_key: Bad API key
            exceptions.bad_id: one or more invalid IDs
            exceptions.bad_parameter: one or more invalid IDs
            requests.exceptions.RequestException: Request error
        """
        if len(ids) > 10:
            raise exceptions.too_many_ids
        # The api has a weird way of constructing URLs with Arrays, thats why I need to manually construct the URL
        # The parameter ids is a string of all the ids, seperated by commas
        idsString = ",".join(ids)
        url = f"{self.BASE_URL}/prices.php?ids={idsString}&apikey={self.api_key}"
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            raise exceptions.api_error(f"HTTP status code: {r.status_code}")

        prices: dict = r.json()

        if prices["ok"] is not True:
            msg = prices["message"]
            if (
                msg == "apikey nicht angegeben, falsch, oder im falschen Format"
                or msg[:38] == "ERROR:  invalid input syntax for uuid:"
            ):
                raise exceptions.invalid_api_key
            if msg == "eine oder mehrere Tankstellen-IDs nicht im korrekten Format":
                raise exceptions.bad_id
            if msg == "parameter error":
                raise exceptions.bad_parameter
            raise exceptions.api_error(msg)

        prices_model = models.Prices_Model(**prices)

        return prices_model
