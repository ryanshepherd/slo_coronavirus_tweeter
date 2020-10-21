import unittest
import json

from __app__ import stats


class TestStats(unittest.TestCase):

    def test_get_stats(self):

        with open("Tests/local.settings.json", "r") as file:
            settings = json.loads(file.read())

        conn_string = settings["TestCovidDBConnectionString"]

        message = stats.Stats(conn_string).get_stats()

        print(message)

        self.assertIsNotNone(message)
        self.assertLess(len(message), 160)
