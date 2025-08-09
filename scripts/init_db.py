import os
import psycopg2
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

DDL_USERS = """
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'client',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
    );
    """

SEED_USERS =[
    ('admin','123','admin'),
    ('guest','guestpass','client')
]

def main():
    #conectamos con la base de datos
    
    with psycopg2.connect(DATABASE_URL) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(DDL_USERS)
            for username, raw_password, role in SEED_USERS:
                password_hash = generate_password_hash(raw_password)
                cur.execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (username) DO NOTHING;
                    """,
                    (username, password_hash, role)
                )



    print('Tabla de usuarios creada y datos inciiales insertados.')
    
if __name__ == "__main__":
    main()
    
