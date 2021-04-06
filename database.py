import psycopg2
from psycopg2.extensions import connection


def get_connection(host, database, user, password) -> connection:
    return psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
