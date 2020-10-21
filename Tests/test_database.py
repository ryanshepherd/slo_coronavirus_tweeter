import unittest
import datetime
import psycopg2
import json

from __app__.SloPageParser import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        with open("Tests/local.settings.json", "r") as file:
            settings = json.loads(file.read())

        self.test_db_conn = settings["TestJunkDBConnectionString"]

        self.quick_sql_command("""
            DROP TABLE IF EXISTS test;
            CREATE TABLE test ("date" date primary key, a int, b int);""")

    def tearDown(self):
        self.quick_sql_command("DROP TABLE IF EXISTS test;")

    def quick_sql_command(self, cmd):
        conn = psycopg2.connect(self.test_db_conn)
        csr = conn.cursor()
        csr.execute(cmd)
        conn.commit()
        csr.close()
        conn.close()

    def get_row_count(self, table):
        conn = psycopg2.connect(self.test_db_conn)
        csr = conn.cursor()
        csr.execute("SELECT COUNT(*) FROM test;")
        result = csr.fetchone()[0]
        csr.close()
        conn.close()
        return result

    def test_upsert_works_for_new_row_insert(self):

        row = { "a": 1, "b": 2 }
        date = datetime.datetime(2020,5,15)

        with database.Database(self.test_db_conn) as db:
            db.upsert_row("test", date, row)

        numrows = self.get_row_count("test")

        self.assertEqual(numrows, 1)

    def test_upsert_works_when_row_exists(self):

        self.quick_sql_command("""INSERT INTO test ("date", a, b) VALUES (CAST('2020-05-15' AS DATE), 3, 4)""")

        row = { "a": 1, "b": 2 }
        date = datetime.datetime(2020,5,15)

        with database.Database(self.test_db_conn) as db:
            db.upsert_row("test", date, row)

        numrows = self.get_row_count("test")

        self.assertEqual(numrows, 1)

    def test_upsert_works_when_dict_contains_extra_keys_not_in_table(self):

        row = { "a": 1, "b": 2, "c": 3 }
        date = datetime.datetime(2020,5,15)

        with database.Database(self.test_db_conn) as db:
            db.upsert_row("test", date, row)

        numrows = self.get_row_count("test")

        self.assertEqual(numrows, 1)

    def test_get_columns_in_table(self):

        with database.Database(self.test_db_conn) as db:
            columns = db.get_columns_in_table("test")

        self.assertEqual(["date", "a", "b"], columns)
