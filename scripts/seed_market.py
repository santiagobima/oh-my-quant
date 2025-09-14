import pandas as pd
import requests
 
URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


response = requests.get(URL, headers=headers)
tables = pd.read_html(response.text)

sp500_table = tables[0]
print(sp500_table.head())