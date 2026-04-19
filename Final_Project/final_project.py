import json
import csv
import os
import requests
import time
from datetime import datetime, timedelta

#-------data building--------

url1 ='https://api.coingecko.com/api/v3/coins/'
url2 ='/history?date='
url3 ='&localization=false'

key1 = 'market_data'
key2 = 'current_price'
key3 = 'usd'

basedt = datetime(2025, 4, 18)

coins = ['bitcoin','ethereum','binancecoin','tron','dogecoin','memecore']

for coin in coins:
    filename = f'{coin}_prices.csv'
    
    #load existing data if present
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add(row['Date'])
   
    #open file in append
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        #header
        if not file_exists:
            writer.writerow(['Date', 'Price_USD'])
    
    #loop through dates to load file
        for i in range(364):
            dt = basedt + timedelta(days=i+1)
            dts = dt.strftime('%d-%m-%Y')
            if dts in existing:
                continue
            url = url1 + coin + url2 + dts + url3
            req = requests.get(url)
            d = json.loads(req.text)
            time.sleep(12)
            try:
                price = d[key1][key2][key3]
                print(dts, d[key1][key2][key3])
                writer.writerow([dts, price])
                f.flush()
                existing.add(dts)
            except Exception as e:
                print(dts, "error: ", e)
