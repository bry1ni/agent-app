import psycopg2
from psycopg2.extras import RealDictCursor

connection_params = {
    "dbname": "your_database",
    "user": "postgres_user",
    "password": "secure_password",
    "host": "localhost",
    "port": "5432"
}

conn = psycopg2.connect(**connection_params) # connection to db
cursor = conn.cursor(cursor_factory=RealDictCursor)