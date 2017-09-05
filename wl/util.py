import mysql.connector
import os


def connect():
    return mysql.connector.connect(
        host=os.environ['DB_HOST'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_DATABASE'],
        ssl_ca='/BaltimoreCyberTrustRoot.crt.pem',
    )


def get_one(cursor):
    return {k: v for k, v in zip(cursor.column_names, cursor.fetchone())}


def get_many(cursor):
    return [{k: v for k, v in zip(cursor.column_names, row)}
            for row in cursor]


class UsingConn:
    """Auto-close a database connection using Python `with`.
    """
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class UsingCursor:
    """Auto-close a database cursor using Python `with`.
    """
    def __init__(self, conn):
        self.conn = conn

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
