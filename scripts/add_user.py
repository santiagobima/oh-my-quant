import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from werkzeug.security import generate_password_hash


load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("DATABASE_URL")    

NEW_USER = ('pepe', 'pepepass', 'client')


username, raw_password, role = NEW_USER
password_hash = generate_password_hash(raw_password)

with psycopg2.connect(DATABASE_URL) as conn:
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (username) DO NOTHING;
            """,
            (username, password_hash, role)
        )
        print(f'Usuario {username} creado o ya existe.')