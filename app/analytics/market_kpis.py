import os 
import psycopg2
import pandas as pd
import numpy as np
import statmodels.api as sm
from datetime import date

def get_prices_df(limit_days=365):
    """Vamos a descargar los precios desde PostgreSQL para los últimos N días"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    query = f"""
        