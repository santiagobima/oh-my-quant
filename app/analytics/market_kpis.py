import os 
import psycopg2
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import date

def get_prices_df(limit_days=365):
    """Vamos a descargar los precios desde PostgreSQL para los últimos N días"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    query = f"""
        SELECT  i.symbol, p.trade_date, p.close
        FROM prices_eod p
        JOIN instruments i ON p.instruments_id = i.id
        WHERE p.trade_date >= CURRENT_DATE - INTERVAL '{limit_days} days'
        ORDER BY i.symbol, p.trade_date;
    """
    
    df = pd.read_sql(query,conn)
    conn.close()
    return df

def calculate_kpis(df):
    """Calcula métricas financieras para cada símbolo."""
    metrics = []
    for symbol, group in df.groupby('symbol'):
        group = group.sort_values('trade_date')
        group['return'] = group['close'].pct_change()
        
        if len(group) < 30:
            continue
        
        daily_returns = group['return'].dropna()
        annual_return = daily_returns.mean() *252
        volatility = daily_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / volatility if volatility != 0 else np.nan
        max_drawdown = (group['close'] / group['close'].cummax() - 1).min()
        
        metrics.append({
            'symbol': symbol,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown    
            
        })
        
    return pd.DataFrame(metrics)
        
        


        