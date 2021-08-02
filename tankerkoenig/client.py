from typing import List
import requests
from . import models
from . import exceptions


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
        petrol_type: models.Petrol,
        sort: models.SortingMethod,
    ) -> models.List_PetrolStations:
        """
        Fetches all petrol stations in a certain radius from a position and returns their prices

        Args:
            lat: Latitude
            lng: Longitude
            rad: Search radius
            petrol_type: Petrol enum
            sort: Sorting enum

        Returns:
          models.PetrolStations: Object with all the petrol stations in the surroundings

        Raises:
            exceptions.api_error: Unspecified error returned from the tankerkoenig API
            exceptions.invalid_api_key: Bad API key
            exceptions.bad_latitude: Latitude out of bounds or wrong format
            exceptions.bad_longitude: Longitude out of bounds or wrong format
            exceptions.bad_radius: Invalid radius
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
        url = f"{self.BASE_URL}/detail.php"
        r = requests.get(url, params={"id": id, "apikey": self.api_key})
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
        if len(ids) > 10:
            raise exceptions.too_many_ids
        # The api has a weird way of constructing URLs with Arrays, thats why I need to manually construct the URL
        # The parameter ids is a string of all the ids, seperated by commas
        idsString = ",".join(ids)
        url = f"{self.BASE_URL}/prices.php?ids={idsString}&apikey={self.api_key}"
        r = requests.get(url)
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
