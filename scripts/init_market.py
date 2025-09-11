import yfinance as yf

df = yf.download("AAPL", period="1mo")
df.columns = df.columns.droplevel(1)
print(df.head())
print(df.columns)