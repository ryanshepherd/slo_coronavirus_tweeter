import psycopg2


class SubscriberRepository:

    def __init__(self, conn_str: str):
        self.conn = psycopg2.connect(conn_str)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def get_subscribers(self):

        sql = """
            SELECT phone
            FROM subscribers;
        """

        cursor = self.conn.cursor()
        cursor.execute(sql)

        return [item[0] for item in cursor.fetchall()]

    def add_subscriber(self, number: str):

        
        sql = """
            INSERT into subscribers (phone)
            VALUES (%s)
        """

        cursor = self.conn.cursor()
        
        try:
            cursor.execute(sql, (number,))
        except psycopg2.Error as e:
            if e.pgcode == "23505":
                return False
            raise(e)

        self.conn.commit()
        
        return True

