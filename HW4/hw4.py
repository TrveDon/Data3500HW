#file reader and ordering
file = open("TSLA.csv")
stockdata = file.readlines()
header = stockdata[0]
body = stockdata[1:]
body.reverse()
stockdata = [header] + body
#isolate close prices
close_prices = [
    float(line.strip().split(',')[1].replace('$', ''))
    for line in stockdata[1:]
]
#Trade logic variables
firstbuy = None
buy = None
profits = []
movwin = 5
#trade logic
for i in range (movwin, len(close_prices)):
    current = close_prices[i]
    prev_5 = close_prices[i -movwin:i]
    ma_5 = sum(prev_5)/movwin

    if current < ma_5 * 0.98:
        if buy is None:
            buy = current
            if firstbuy is None:
                firstbuy= current
            print('buying at: ',current, 'Iteration', i)
        else:
            print('Holding at current price')
    elif current > ma_5 *1.02:
        if buy is not None:
            sell = current
            pro = sell-buy
            profits.append(pro)
            print('selling at: ',current)
            buy = None
        else:
            print('No stock to sell')
    else:
        print("holding current price")
#sums and outputs
total_profit = sum(profits)
print('first buy price: ',firstbuy)
print('Total profit: ',total_profit)
percent =(total_profit/ firstbuy) * 100
print('Percent return: ', percent)