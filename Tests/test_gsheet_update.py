import unittest
import json
from __app__.GSheetUpdater import google_sheets

class TestGSheetUpdate(unittest.TestCase):

    def test_update(self):
        workbook_name = "SLO Coronavirus Cases - Dev"
        cities_list = "paso_robles,san_luis_obispo_city,nipomo,atascadero,arroyo_grande,san_miguel,grover_beach,templeton,pismo_beach,oceano,los_osos,ca_mens_colony_inmates,morro_bay,cambria,santa_margarita,shandon,cayucos,avila,creston,san_simeon,under_investigation,other"

        data = {
            "date": "2020-08-08",
            "status": {
                "total": 30,
                "recovered": 20,
                "deaths": 10
            },
            "cities": {
                "ca_mens_colony_inmates": 12,
                "morro_bay": 13,
                "cambria": 14,
                "santa_margarita": 15,
                "shandon": 16,
                "cayucos": 17,
                "avila": 18,
                "creston": 19,
                "san_simeon": 20,
                "under_investigation": 21,
                "other": 22,
                "paso_robles": 1,
                "san_luis_obispo_city": 2,
                "nipomo": 3,
                "atascadero": 4,
                "arroyo_grande": 5,
                "san_miguel": 6,
                "grover_beach": 7,
                "templeton": 8,
                "pismo_beach": 9,
                "oceano": 10,
                "los_osos": 11
            },
            "tests": {
                "slo_public_health_lab_positive": 4,
                "slo_public_health_lab_negative": 4,
                "outside_labs_positive": 4,
                "outside_labs_negative": 4
            }
        }

        with open("__app__/google_client_secret.json", "r") as file:
            client_secret = json.loads(file.read())

        try:
            google_sheets.update_sheets(data, cities_list, workbook_name, client_secret)
        except Exception as e:
            self.assertFalse(e)
        
        self.assertTrue("No errors thrown!")