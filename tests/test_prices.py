from tankerkoenig import client, models, exceptions
from unittest import TestCase
from os import getenv
import responses


class TestPrices(TestCase):
    maxDiff = None

    def setUp(self):
        self.api_key = getenv("TANKERKOENIG_API_KEY")
        self.client = client.Client(api_key=self.api_key)

    @responses.activate
    def test_prices(self):
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/prices.php",
            body='{"ok":true,"license":"CC BY 4.0 -  https:\/\/creativecommons.tankerkoenig.de","data":"MTS-K","prices":{"3a96b82f-7342-40ba-a1d7-9cde3fbb3c11":{"status":"open","e5":1.619,"e10":1.559,"diesel":1.389},"5d73b461-5646-4b7b-a98d-aa866b87fdd3":{"status":"open","e5":1.639,"e10":1.579,"diesel":1.439}}}',
            status=200,
            content_type="application/json",
        )

        res: models.Prices_Model = self.client.prices(
            ids=[
                "3a96b82f-7342-40ba-a1d7-9cde3fbb3c11",
                "5d73b461-5646-4b7b-a98d-aa866b87fdd3",
            ]
        )
        req_url = responses.calls[0].request.url

        EXPECTED_URL = f"https://creativecommons.tankerkoenig.de/json/prices.php?ids=3a96b82f-7342-40ba-a1d7-9cde3fbb3c11,5d73b461-5646-4b7b-a98d-aa866b87fdd3&apikey={self.api_key}"
        self.assertEqual(req_url, EXPECTED_URL)

    @responses.activate
    def test_bad_api_key(self):
        tmp_client = client.Client(api_key="definitely-not-a-real-key")

        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/prices.php",
            body='{"status":"error","ok":false,"message":"ERROR:  invalid input syntax for uuid: definitely-not-a-real-key"}',
            status=200,
            content_type="application/json",
        )
        with self.assertRaises(exceptions.invalid_api_key):
            _ = tmp_client.prices(ids=["3a96b82f-7342-40ba-a1d7-9cde3fbb3c11"])

    @responses.activate
    def test_prices_bad_id(self):
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/prices.php",
            body='{"status":"error","ok":false,"message":"parameter error"}',
            status=200,
            content_type="application/json",
        )
        with self.assertRaises(exceptions.bad_parameter):
            _ = self.client.prices(ids=["notAREalID"])
