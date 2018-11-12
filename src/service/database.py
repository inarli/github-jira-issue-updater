import psycopg2
import os


class database:

    def connect(self):
        return psycopg2.connect(dsn=os.getenv('DATABASE_URL'))
