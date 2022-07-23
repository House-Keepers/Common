import pyodbc
from src.SQLHandler.Query import Query

class SQLClient:
    def __init__(self, server: str, database: str, username: str, password: str, port: int = 1433,
                 driver: str = "{ODBC Driver 17 for SQL Server}"):
        self.__connection_string = f'DRIVER={driver};SERVER=tcp:{server};PORT={port};DATABASE={database};UID={username};PWD={password} '

    def query(self, query: Query):
        with pyodbc.connect(self.__connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query.build())
                if query.query_type() == 'select':
                    return cursor.fetchall()
                cursor.commit()
