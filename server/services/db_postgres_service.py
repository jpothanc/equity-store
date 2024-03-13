import psycopg2
from services.database_service import DatabaseService


class DbPostgresService(DatabaseService):
    def __init__(self):
        pass
    def query(self, connection_string, query):
        with psycopg2.connect(connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                col_names = [desc[0] for desc in cur.description]
                return col_names, cur.fetchall()
