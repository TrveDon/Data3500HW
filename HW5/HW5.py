import json

# Mean Reversion Strategy
def meanReversionStrategy(prices, ticker="TICKER"):
    print(f"\n{ticker} Mean Reversion Strategy Output:")

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
                print(f"buying at:       {round(price, 2)}")

        elif price > avg * 1.02:
            if buy is not None:
                sell = price
                profit = sell - buy
                profits.append(profit)

                print(f"selling at:      {round(sell, 2)}")
                print(f"trade profit:    {round(profit, 2)}")

                buy = None

    total_profit = sum(profits)
    percent = (total_profit / firstbuy * 100) if firstbuy else 0

    print("-----------------------")
    print(f"Total profit:    {round(total_profit, 2)}")
    print(f"First buy:       {round(firstbuy, 2) if firstbuy else 0}")
    print(f"Percent return:  {round(percent, 2)}")

    return total_profit, percent

# Simple Moving Average Strategy

def simpleMovingAverageStrategy(prices, ticker="TICKER"):
    print(f"\n{ticker} Simple Moving Average Strategy Output:")

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
                print(f"buying at:       {round(price, 2)}")

        elif price < avg:
            if buy is not None:
                sell = price
                profit = sell - buy
                profits.append(profit)

                print(f"selling at:      {round(sell, 2)}")
                print(f"trade profit:    {round(profit, 2)}")

                buy = None

    total_profit = sum(profits)
    percent = (total_profit / firstbuy * 100) if firstbuy else 0

    print("-----------------------")
    print(f"Total profit:    {round(total_profit, 2)}")
    print(f"First buy:       {round(firstbuy, 2) if firstbuy else 0}")
    print(f"Percent return:  {round(percent, 2)}")

    return total_profit, percent


# Save Results
def saveResults(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

# File Reader
def load_prices(filename):
    with open(filename) as file:
        lines = file.readlines()

    header = lines[0]
    body = lines[1:]
    body.reverse()
    data = [header] + body

    prices = [
        float(line.strip().split(',')[1].replace('$', '').replace('"', ''))
        for line in data[1:]
    ]

    return prices

# Main Program
tickers = ["CISCO"]  # you can expand to 10 tickers

results = {}

for ticker in tickers:
    prices = load_prices(f"HW5/{ticker}.csv")

    results[f"{ticker}_prices"] = prices

    sma_profit, sma_returns = simpleMovingAverageStrategy(prices, ticker)
    results[f"{ticker}_sma_profit"] = sma_profit
    results[f"{ticker}_sma_returns"] = sma_returns

    mr_profit, mr_returns = meanReversionStrategy(prices, ticker)
    results[f"{ticker}_mr_profit"] = mr_profit
    results[f"{ticker}_mr_returns"] = mr_returns

# save at end
saveResults(results)