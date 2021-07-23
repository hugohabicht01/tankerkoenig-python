import tankerkoenig
from tankerkoenig import client, exceptions, models
from unittest import TestCase
from os import getenv
import responses


class TestList(TestCase):
    maxDiff = None

    def setUp(self):
        self.api_key = getenv("TANKERKOENIG_API_KEY")
        self.client = tankerkoenig.Client(api_key=self.api_key)

    @responses.activate
    def test_list(self):
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/list.php",
            body='{"ok":true,"license":"CC BY 4.0 -  https:\/\/creativecommons.tankerkoenig.de","data":"MTS-K","status":"ok","stations":[{"id":"3a96b82f-7342-40ba-a1d7-9cde3fbb3c11","name":"Aral Tankstelle","brand":"ARAL","street":"Hanauer Landstra\u00dfe","place":"Frankfurt","lat":50.1129227,"lng":8.699732,"dist":0.9,"price":1.419,"isOpen":true,"houseNumber":"34-40","postCode":60314},{"id":"5d73b461-5646-4b7b-a98d-aa866b87fdd3","name":"Aral Tankstelle","brand":"ARAL","street":"Siemensstra\u00dfe","place":"Frankfurt","lat":50.10236,"lng":8.695524,"dist":1.5,"price":1.419,"isOpen":true,"houseNumber":"37","postCode":60594},{"id":"09978ef8-5fa5-46d5-8389-957eb7cd8540","name":"Aral Tankstelle","brand":"ARAL","street":"Grueneburgweg","place":"Frankfurt","lat":50.12197,"lng":8.669096,"dist":1.6,"price":1.419,"isOpen":true,"houseNumber":"67","postCode":60323},{"id":"cad634d9-1a5a-49dd-a4ec-1de12d61eff0","name":"Shell Frankfurt Am Main Moerfelder Landstr. 16","brand":"Shell","street":"Moerfelder Landstr.","place":"Frankfurt Am Main","lat":50.100418,"lng":8.690331,"dist":1.6,"price":1.429,"isOpen":true,"houseNumber":"16","postCode":60598},{"id":"0e41a6a4-e678-4dce-8568-020210c6cee9","name":"Shell Frankfurt Am Main Friedberger Landstr. 152","brand":"Shell","street":"Friedberger Landstr.","place":"Frankfurt Am Main","lat":50.129887,"lng":8.694316,"dist":1.8,"price":1.429,"isOpen":true,"houseNumber":"152","postCode":60389},{"id":"0a70f16c-0b9e-4083-973e-01173c8839e5","name":"Esso Tankstelle","brand":"ESSO","street":"SPESSARTSTR. 22-24","place":"FRANKFURT","lat":50.12519,"lng":8.709553,"dist":2,"price":1.419,"isOpen":true,"houseNumber":"","postCode":60385},{"id":"2fdeef9e-36ca-44d7-9ee4-3bdaa0112539","name":"TotalEnergies Frankfurt","brand":"TOTAL","street":"Eckenheimer Landstr. 181","place":"Frankfurt","lat":50.13218,"lng":8.683576,"dist":2,"price":1.429,"isOpen":true,"houseNumber":"","postCode":60320}]}',
            status=200,
            content_type="application/json",
        )

        # 50.114634, 8.687657 = Konstabler Wache Frankfurt
        params = {
            "lat": 50.114634,
            "lng": 8.687657,
            "rad": 2,
            "petrol_type": models.Petrol.DIESEL,
            "sort": models.SortingMethod.DISTANCE,
        }
        _ = self.client.list(**params)
        req_url = responses.calls[0].request.url

        EXPECTED_URL = f"https://creativecommons.tankerkoenig.de/json/list.php?lat=50.114634&lng=8.687657&rad=2&sort=dist&type=diesel&apikey={self.api_key}"
        self.assertEqual(req_url, EXPECTED_URL)

        # EXPECTED_RES = """{"ok": true,"license": "CC BY 4.0 -  https: \/\/creativecommons.tankerkoenig.de","data": "MTS-K","status": "ok","stations": [{"id": "3a96b82f-7342-40ba-a1d7-9cde3fbb3c11","name": "Aral Tankstelle","brand": "ARAL","street": "Hanauer Landstra\u00dfe","place": "Frankfurt","lat": 50.1129227,"lng": 8.699732,"dist": 0.9,"price": 1.419,"isOpen": true,"houseNumber": "34-40","postCode": 60314},{"id": "5d73b461-5646-4b7b-a98d-aa866b87fdd3","name": "Aral Tankstelle","brand": "ARAL","street": "Siemensstra\u00dfe","place": "Frankfurt","lat": 50.10236,"lng": 8.695524,"dist": 1.5,"price": 1.419,"isOpen": true,"houseNumber": "37","postCode": 60594},{"id": "09978ef8-5fa5-46d5-8389-957eb7cd8540","name": "Aral Tankstelle","brand": "ARAL","street": "Grueneburgweg","place": "Frankfurt","lat": 50.12197,"lng": 8.669096,"dist": 1.6,"price": 1.419,"isOpen": true,"houseNumber": "67","postCode": 60323},{"id": "cad634d9-1a5a-49dd-a4ec-1de12d61eff0","name": "Shell Frankfurt Am Main Moerfelder Landstr. 16","brand": "Shell","street": "Moerfelder Landstr.","place": "Frankfurt Am Main","lat": 50.100418,"lng": 8.690331,"dist": 1.6,"price": 1.429,"isOpen": true,"houseNumber": "16","postCode": 60598},{"id": "0e41a6a4-e678-4dce-8568-020210c6cee9","name": "Shell Frankfurt Am Main Friedberger Landstr. 152","brand": "Shell","street": "Friedberger Landstr.","place": "Frankfurt Am Main","lat": 50.129887,"lng": 8.694316,"dist": 1.8,"price": 1.429,"isOpen": true,"houseNumber": "152","postCode": 60389},{"id": "0a70f16c-0b9e-4083-973e-01173c8839e5","name": "Esso Tankstelle","brand": "ESSO","street": "SPESSARTSTR. 22-24","place": "FRANKFURT","lat": 50.12519,"lng": 8.709553,"dist": 2,"price": 1.419,"isOpen": true,"houseNumber": "","postCode": 60385},{"id": "2fdeef9e-36ca-44d7-9ee4-3bdaa0112539","name": "TotalEnergies Frankfurt","brand": "TOTAL","street": "Eckenheimer Landstr. 181","place": "Frankfurt","lat": 50.13218,"lng": 8.683576,"dist": 2,"price": 1.429,"isOpen": true,"houseNumber": "","postCode": 60320}]}"""
        # self.assertDictEqual(a, b)

    @responses.activate
    def test_list_bad_api_key(self):
        # Mock API instead of actually running the request
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/list.php",
            body='{"status":"error","ok":false,"message":"apikey nicht angegeben, falsch, oder im falschen Format"}',
            status=200,
            content_type="application/json",
        )
        tmp_client = client.Client(api_key="definitelyNotARealKey")
        params = {
            "lat": 50.114634,
            "lng": 8.687657,
            "rad": 2,
            "petrol_type": models.Petrol.DIESEL,
            "sort": models.SortingMethod.DISTANCE,
        }

        with self.assertRaises(exceptions.invalid_api_key):
            _ = tmp_client.list(**params)

    @responses.activate
    def test_list_bad_coordinates(self):
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/list.php",
            body='{"status":"error","ok":false,"message":"lat nicht angegeben, oder ausserhalb der g\u00fcltigen Grenzen"}',
            status=200,
            content_type="application/json",
        )
        params = {
            "lat": "NotARealCoordinate",
            "lng": 8.687657,
            "rad": 2,
            "petrol_type": models.Petrol.DIESEL,
            "sort": models.SortingMethod.DISTANCE,
        }
        with self.assertRaises(exceptions.bad_latitude):
            _ = self.client.list(**params)

    @responses.activate
    def test_list_bad_radius(self):
        # Mock API instead of actually running the request
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/list.php",
            body='{"status":"error","ok":false,"message":"rad nicht angegeben, oder ausserhalb des g\u00fcltigen Bereichs"}',
            status=200,
            content_type="application/json",
        )
        params = {
            "lat": 50.114634,
            "lng": 8.687657,
            "rad": -2,
            "petrol_type": models.Petrol.DIESEL,
            "sort": models.SortingMethod.DISTANCE,
        }
        with self.assertRaises(exceptions.bad_radius):
            _ = self.client.list(**params)
