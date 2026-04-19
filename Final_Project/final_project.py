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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

basedt = datetime(2025, 4, 18)

coins = ['bitcoin','ethereum','binancecoin','tron','dogecoin','tether']

def build_data():   
    for coin in coins: 
        filename = os.path.join(BASE_DIR, f'{coin}_prices.csv')
    
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
                    print(f"[{coin}] {dts} {price}")
                    writer.writerow([dts, price])
                    f.flush()
                    existing.add(dts)
                except Exception as e:
                    print(dts, "error: ", e)

#------------File Loader---------
def load_prices(filename):
    prices = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                prices.append(float(row["Price_USD"]))
            except:
                continue
    return prices

# ------ Simple Moving Average---------

def SMA(prices, ticker = 'TICKER'):
    buy = None
    firstbuy = None
    profits = []
    movwin = 5

    for i in range(movwin, len(prices)):
        price = prices[i]
        avg = sum(prices[i - movwin:i]) / movwin

        if price > avg:
            if buy is None:
                buy = price
                if firstbuy is None:
                    firstbuy = price

        elif price < avg:
            if buy is not None:
                sell = price
                profits.append(sell - buy)
                buy = None

    return profits, firstbuy

#------- Mean Reversion-------
def MRstrat(prices, ticker = 'TICKER'):
    buy = None
    firstbuy = None
    profits = []
    movwin = 5

    for i in range(movwin, len(prices)):
        price = prices[i]
        avg = sum(prices[i - movwin:i]) / movwin

        if price < avg * 0.98:
            if buy is None:
                buy = price
                if firstbuy is None:
                    firstbuy = price

        elif price > avg * 1.02:
            if buy is not None:
                sell = price
                profits.append(sell - buy)
                buy = None

    return profits, firstbuy

#------Metrics calculation------
def compute_metrics(profits, firstbuy):
    if not profits or not firstbuy:
        return 0, 0, 0

    total_profit = sum(profits)
    returns = (total_profit / firstbuy) * 100

    wins = len([p for p in profits if p > 0])
    win_rate = (wins / len(profits)) * 100 if profits else 0

    equity = 0
    peak = 0
    max_dd = 0

    for p in profits:
        equity += p
        peak = max(peak, equity)
        max_dd = max(max_dd, peak - equity)

    drawdown = (max_dd / firstbuy) * 100 if firstbuy else 0

    return returns, win_rate, drawdown

#------Save results-----
def saveResults(results):
    filepath = os.path.join(BASE_DIR, "finalres.json")
    with open(filepath, "w") as f:
        json.dump(results, f, indent=4)

#------Main Systems-----
def main():
    print("Building / updating data...")
    build_data()

    results = {}
    scores = {}

    for coin in coins:
        filename = os.path.join(BASE_DIR, f"{coin}_prices.csv")

        if not os.path.exists(filename):
            continue

        prices = load_prices(filename)

        # SMA
        sma_profits, sma_firstbuy = SMA(prices, coin)
        sma_ret, sma_win, sma_dd = compute_metrics(sma_profits, sma_firstbuy)

        sma_score = (sma_ret * 0.5) + (sma_win * 30) - (sma_dd * 20)

        # MR
        mr_profits, mr_firstbuy = MRstrat(prices, coin)
        mr_ret, mr_win, mr_dd = compute_metrics(mr_profits, mr_firstbuy)

        mr_score = (mr_ret * 0.5) + (mr_win * 30) - (mr_dd * 20)

        results[f"{coin}_sma_score"] = sma_score
        results[f"{coin}_mr_score"] = mr_score

        scores[(coin, "SMA")] = sma_score
        scores[(coin, "MR")] = mr_score

    saveResults(results)

#------Final output------
    best = max(scores, key=scores.get)
    best_coin, best_strategy = best
    best_score = scores[best]

    strategy_name = "Simple Moving Average" if best_strategy == "SMA" else "Mean Reversion"

    print("Trade Results")
    print(f"Best Coin:      {best_coin.upper()}")
    print(f"Best Strategy:  {strategy_name}")
    print(f"Score:          {round(best_score, 2)}")

#------Safe Entry------

if __name__ == "__main__":
    main()