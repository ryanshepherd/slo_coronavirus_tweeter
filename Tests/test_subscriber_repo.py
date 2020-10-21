import unittest
import json
import psycopg2

from __app__ import subscriber_repo


class TestSubcriberRepo(unittest.TestCase):

    def setUp(self):
        with open("Tests/local.settings.json", "r") as file:
            settings = json.loads(file.read())

        self.test_db_conn = settings["TestCovidDBConnectionString"]      

    def quick_sql_command(self, cmd):
        conn = psycopg2.connect(self.test_db_conn)
        csr = conn.cursor()
        csr.execute(cmd)
        conn.commit()
        csr.close()
        conn.close()

    def test_get_subscribers(self):

        with subscriber_repo.SubscriberRepository(self.test_db_conn) as repo:
            subscribers = repo.get_subscribers()

        self.assertEqual(len(subscribers), 1)
        self.assertEqual(subscribers[0], "+14088401722")

    def test_add_new_subscriber(self):

        with subscriber_repo.SubscriberRepository(self.test_db_conn) as repo:
            success = repo.add_subscriber("+1xxxyyyzzzz")

        self.assertTrue(success)
        
        # Cleanup
        self.quick_sql_command("DELETE FROM subscribers WHERE phone = '+1xxxyyyzzzz'")

    def test_existing_subscriber(self):

        with subscriber_repo.SubscriberRepository(self.test_db_conn) as repo:
            success = repo.add_subscriber("+14088401722")

        self.assertFalse(success)
