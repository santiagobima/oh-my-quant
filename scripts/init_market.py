import os 
import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv('DATABASE_URL')

DDL_INSTRUMENTS = """
CREATE TABLE IF NOT EXISTS instruments (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100),
    kind VARCHAR(20) DEFAULT 'equity',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

DDL_PRICES_EOD = """
CREATE TABLE IF NOT EXISTS prices_eod (
    id SERIAL PRIMARY KEY,
    instrument_id INT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    trade_date DATE NOT NULL,
    open NUMERIC(18,6),
    high NUMERIC(18,6),
    low NUMERIC(18,6),
    close NUMERIC(18,6),
    adj_close NUMERIC(18,6),
    volume BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (instrument_id, trade_date)
);
"""


def main():
    if not DATABASE_URL:
        raise RuntimeError('DATABASE_URL no está definido en. env')
    
    with psycopg2.connect(DATABASE_URL) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(DDL_INSTRUMENTS)
            cur.execute(DDL_PRICES_EOD)
            
        print("Tablas de mercado creadas correctamente.")

if __name__ == "__main__":
    main()
    




