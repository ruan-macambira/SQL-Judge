import psycopg2
from lib.adapter import DBAdapter

class PostgresAdapter(DBAdapter):
    """ Database Adapter to a Postgress database """
    def __init__(self, host: str, database: str, username: str, password: str, port:str):
        self.host = host
        self.database = database
        self.username = username
        self.password = password
        self.port = port

    def connection(self):
        return psycopg2.connect(
            host=self.host, dbname=self.database, port=self.port,
            user=self.username, password=self.password
        )

    def execute(self, sql):
        conn = self.connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        ret = []
        for query_row in cursor.fetchall():
            auy = {}
            for i in range(len(cursor.description)):
                auy[cursor.description[i][0]] = query_row[i]
            ret.append(auy)
        cursor.close()
        conn.close()

        return ret

    def tables(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = \'public\'"

        return [row['table_name'].upper() for row in self.execute(sql)]

    def columns(self, _table_name):
        return []
