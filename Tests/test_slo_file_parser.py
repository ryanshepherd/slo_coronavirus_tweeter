import unittest
import datetime
import os
from __app__.SloPageParser import slo_file_parser


class TestSloFileParser(unittest.TestCase):

    def test_v1a_date_retrieval(self):
        with open("TestFiles/PageSnapshots/20200429_slo_v1a.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)

        self.assertEqual(page.update_date, datetime.datetime(2020, 4, 29))

    def test_v1a_get_status(self):
        with open("TestFiles/PageSnapshots/20200429_slo_v1a.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_status()

        expected = {
            "total": 181,
            "recovered": 135,
            "deaths": 1,
            "icu": 0,
            "hospitalized": 5
        }

        self.assertEqual(actual, expected)

    def test_v1a_get_cities(self):
        with open("TestFiles/PageSnapshots/20200429_slo_v1a.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_cities()

        expected = {            
            'paso_robles': 58,
            'atascadero': 31,
            'arroyo_grande': 19,
            'nipomo': 14,
            'san_luis_obispo_city': 14,
            'ca_mens_colony_inmates': 8,
            'templeton': 7,
            'san_miguel': 7,
            'pismo_beach': 7,
            'morro_bay': 6,
            'other': 10
        }

        self.assertEqual(actual, expected)

    def test_v1a_get_transmission_type(self):
        with open("TestFiles/PageSnapshots/20200429_slo_v1a.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_transmission_type()

        expected = {
            'travel': 49,
            'person_to_person': 73,
            'community': 59,
            'unknown': 0
        }

        self.assertEqual(actual, expected)

    def test_v1a_get_lab_tests(self):
        with open("TestFiles/PageSnapshots/20200429_slo_v1a.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_tests()

        expected = {
            'slo_public_health_lab_positive': 62,
            'private_labs_positive': 119,
            'slo_public_health_lab_negative': 1152,
            'private_labs_negative': 1489
        }

        self.assertEqual(actual, expected)


    def test_v1b_date_retrieval(self):
        with open("TestFiles/PageSnapshots/20200612_slo_v1b.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)

        self.assertEqual(page.update_date, datetime.datetime(2020, 6, 12))

    def test_v2_get_status(self):
        with open("TestFiles/PageSnapshots/20200703_slo_v2.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_status()

        expected = {
            "total": 1112,
            "recovered": 484,
            "deaths": 2,
            "icu": 6,
            "hospitalized": 9
        }

        self.assertEqual(actual, expected)

    def test_v2_get_cities(self):
        with open("TestFiles/PageSnapshots/20200703_slo_v2.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_cities()

        expected = {
            'paso_robles': 175,
            'san_luis_obispo_city': 110,
            'nipomo': 106,
            'atascadero': 75,
            'arroyo_grande': 54,
            'grover_beach': 25,
            'templeton': 24,
            'pismo_beach': 21,
            'san_miguel': 20,
            'los_osos': 15,
            'oceano': 15,
            'ca_mens_colony_inmates': 11,
            'morro_bay': 10,
            'cambria': 7,
            'shandon': 6,
            'cayucos': 6,
            'unknown': 2,
            'other': 19
        }

        self.assertEqual(actual, expected)

    def test_v2_get_transmission_type(self):
        with open("TestFiles/PageSnapshots/20200703_slo_v2.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_transmission_type()

        expected = {
            'travel': 78,
            'person_to_person': 282,
            'community': 230,
            'unknown': 112
        }

        self.assertEqual(actual, expected)

    def test_v2_get_lab_tests(self):
        with open("TestFiles/PageSnapshots/20200703_slo_v2.html", "r") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_tests()

        expected = {
            'slo_public_health_lab_positive': 133,
            'outside_labs_positive': 542,
            'slo_public_health_lab_negative': 5536,
            'outside_labs_negative': 17937
        }

        self.assertEqual(actual, expected)


    def test_v3_date_retrieval(self):
        with open("TestFiles/PageSnapshots/20200818_slo_v3.html", "r", encoding="utf-8") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)

        self.assertEqual(page.update_date, datetime.datetime(2020, 8, 18))

    def test_v3_get_status(self):
        with open("TestFiles/PageSnapshots/20200818_slo_v3.html", "r", encoding="utf-8") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_status()

        expected = {
            "total": 2571,
            "recovered": 2095,
            "deaths": 19,
            "icu": 5,
            "hospitalized": 15
        }

        self.assertEqual(actual, expected)

    def test_v3_get_cities(self):
        with open("TestFiles/PageSnapshots/20200818_slo_v3.html", "r", encoding="utf-8") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_cities()

        expected = {
            'paso_robles': 669,
            'nipomo': 295,
            'san_luis_obispo_city': 290,
            'atascadero': 286,
            'cmc_inmates': 219,
            'arroyo_grande': 173,
            'grover_beach': 121,
            'templeton': 99,
            'san_miguel': 95,
            'oceano': 84,
            'pismo_beach': 49,
            'los_osos': 46,
            'morro_bay': 34,
            'cambria': 29,
            'santa_margarita': 23,
            'shandon': 16,                  
            'cayucos': 14,
            'avila': 8,
            'san_simeon': 6,
            'under_investigation': 4,
            'other': 11
        }

        self.assertEqual(actual, expected)

    def test_v3_get_transmission_type(self):
        with open("TestFiles/PageSnapshots/20200818_slo_v3.html", "r", encoding="utf-8") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_transmission_type()

        expected = {
            'travel': 184,
            'person_to_person': 1190,
            'community': 718,
            'unknown': 479
        }

        self.assertEqual(actual, expected)

    def test_v3_get_lab_tests(self):
        with open("TestFiles/PageSnapshots/20200818_slo_v3.html", "r", encoding="utf-8") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_tests()

        expected = {
            'slo_public_health_lab_positive': 292,
            'outside_labs_positive': 2279,
            'slo_public_health_lab_negative': 11786,
            'outside_labs_negative': 34846
        }

        self.assertEqual(actual, expected)

    def test_v4_get_status(self):
        with open("TestFiles/PageSnapshots/20200914_slo_v4.html", "r", encoding="UTF-8") as file:
            content = file.read()

        page = slo_file_parser.SloPage(content)
        actual = page.get_status()

        expected = {
            "total": 3278,
            "recovered": 3048,
            "deaths": 26,
            "icu": 3,
            "hospitalized": 8,
            "test_positivity": 4.6
        }

        self.assertEqual(actual, expected)