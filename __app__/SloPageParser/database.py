import psycopg2
import datetime
import logging


class Database():

    def __init__(self, conn_str: str):
        self.conn = psycopg2.connect(conn_str)

    def upsert_row(self, table_name: str, date: datetime.date, data: dict):

        # Copy the data to avoid modifying the referenced data
        data = data.copy()
        data["date"] = date
        
        csr = self.conn.cursor()

        try:

            # Remove row if exists
            sql = f"""DELETE FROM {table_name} WHERE "date" = '{str(date)[0:10]}';"""
            csr.execute(sql)
            self.conn.commit()

            # Only attempt to insert into columns that exist
            existing_columns = self.get_columns_in_table(table_name)

            # Define a new dictionary that contains only the existing columns
            new_data = {k: data[k]
                        for k in data.keys() if k in existing_columns}

            # Log a warning if there are extra columns
            if len(new_data) < len(data):
                logging.warn("The following columns don't exist in target table. Skipping: " +
                             ", ".join([k for k in data.keys() if k not in existing_columns]))

            # Save dict to table
            placeholders = ', '.join(['%s'] * len(new_data))
            columns = ', '.join(['"' + k + '"' for k in new_data.keys()])
            sql = f"""
                INSERT INTO {table_name} ( {columns} )
                VALUES ( {placeholders} );
            """

            csr.execute(sql, (list(new_data.values())))
            self.conn.commit()
            csr.close()

        except:
            self.conn.rollback()
            csr.close()
            raise

    def get_columns_in_table(self, table_name: str) -> dict:

        schema = "public"
        sql = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s and TABLE_NAME = %s;"

        cursor = self.conn.cursor()
        cursor.execute(sql, (schema, table_name))
        results = [item[0] for item in cursor.fetchall()]
        cursor.close()

        return results

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
