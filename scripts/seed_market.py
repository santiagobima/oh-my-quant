import pandas as pd
import requests
import os
import psycopg2
import yfinance as yf
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
DATABASE_URL = os.getenv("DATABASE_URL")

def safe_float(value):
    try:
        return float(value) if pd.notna(value) else None
    
    except Exception:
        return None


def main():
    if not DATABASE_URL:
        raise RuntimeError('Database no está definido en .env')
    

# Descargamos la tabla de S&P 500 desde Wikipedia.
 
URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


response = requests.get(URL, headers=headers)
tables = pd.read_html(response.text)
sp500_table = tables[0]
df = sp500_table[['Symbol','Security']].copy()
df['kind'] = 'equity'
df.rename(columns={'Symbol': 'symbol', 'Security': 'name'}, inplace = True)
df_symbols = df.copy()

print(df_symbols.head())



with psycopg2.connect(DATABASE_URL) as conn:
    conn.autocommit = True
    with conn.cursor() as cur:
        for _, row in df_symbols.iterrows():
            symbol = row['symbol']
            name = row['name']
            kind = row['kind']
            
            cur.execute("""
                INSERT INTO instruments (symbol, name, kind)
                VALUES (%s,%s,%s)
                ON CONFLICT (symbol) DO NOTHING
                RETURNING id;
            """, (symbol, name, kind))
            
            if cur.rowcount > 0:
                instrument_id = cur.fetchone()[0]
                print(f"Inserted instrument {symbol} with ID {instrument_id}")
            else:
                cur.execute('SELECT id FROM instruments WHERE symbol = %s', (symbol,))
                instrument_id = cur.fetchone()[0]
                print(f"Instrument {symbol} already exists with ID {instrument_id}")  
            
            try:
                yf_symbol = symbol.replace('.', '-')
                data = yf.download(yf_symbol, period='1Y')
                print("Columnas originales:", data.columns.tolist())
                data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]
                print(f' Downloaded {len(data)} rows for {symbol}')
                for date, row in data.iterrows():
                    trade_date = date.date()
                    open_ = float(row['Open']) if not pd.isna(row['Open']) else None
                    high = float(row['High']) if not pd.isna(row['High']) else None
                    low = float(row['Low']) if not pd.isna(row['Low']) else None
                    close = float(row['Close']) if not pd.isna(row['Close']) else None
                    volume = int(row['Volume']) if not pd.isna(row['Volume']) else None
                    
                    cur.execute("""
                                INSERT INTO prices_eod
                                (instrument_id, trade_date, open,high,low, close ,volume)
                                VALUES (%s,%s,%s,%s,%s,%s,%s)
                                ON CONFLICT (instrument_id, trade_date) DO NOTHING;
                                """, (instrument_id, trade_date, open_, high, low , close, volume))
                    print(f' Inserted {cur.rowcount} rows for {symbol}')
                                
            except Exception as e:
                print(f"Error downloading {symbol}: {e}")


if __name__ == '__main__':
    main()
    


