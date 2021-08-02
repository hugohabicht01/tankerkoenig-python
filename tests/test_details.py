from tankerkoenig import client, models, exceptions
from unittest import TestCase
from os import getenv
import responses


class TestDetails(TestCase):
    maxDiff = None

    def setUp(self):
        self.api_key = getenv("TANKERKOENIG_API_KEY")
        self.client = client.Client(api_key=self.api_key)

    @responses.activate
    def test_details(self):
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/detail.php",
            body='{"ok":true,"license":"CC BY 4.0 -  https:\\/\\/creativecommons.tankerkoenig.de","data":"MTS-K","status":"ok","station":{"id":"3a96b82f-7342-40ba-a1d7-9cde3fbb3c11","name":"Aral Tankstelle","brand":"ARAL","street":"Hanauer Landstra\\u00dfe","houseNumber":"34-40","postCode":60314,"place":"Frankfurt","openingTimes":[{"text":"t\\u00e4glich","start":"06:00:00","end":"23:00:00"}],"overrides":[],"wholeDay":false,"isOpen":true,"e5":1.689,"e10":1.629,"diesel":1.449,"lat":50.1129227,"lng":8.699732,"state":null}}',
            status=200,
            content_type="application/json",
        )

        _ = self.client.details(id="3a96b82f-7342-40ba-a1d7-9cde3fbb3c11")
        req_url = responses.calls[0].request.url

        EXPECTED_URL = f"https://creativecommons.tankerkoenig.de/json/detail.php?id=3a96b82f-7342-40ba-a1d7-9cde3fbb3c11&apikey={self.api_key}"
        self.assertEqual(req_url, EXPECTED_URL)

    @responses.activate
    def test_details_bad_api_key(self):
        tmp_client = client.Client(api_key="definitelyNotARealKey")

        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/detail.php",
            body='{"status":"error","ok":false,"message":"ERROR:  invalid input syntax for uuid: \\"847afb09-63d9-2f42-8f6c-\\""}',
            status=200,
            content_type="application/json",
        )
        with self.assertRaises(exceptions.invalid_api_key):
            _ = tmp_client.details(id="3a96b82f-7342-40ba-a1d7-9cde3fbb3c11")

    @responses.activate
    def test_details_bad_id(self):
        responses.add(
            responses.GET,
            "https://creativecommons.tankerkoenig.de/json/detail.php",
            body='{"status":"error","ok":false,"message":"parameter error"}',
            status=200,
            content_type="application/json",
        )
        with self.assertRaises(exceptions.bad_id):
            _ = self.client.details(id="notAREalID")
