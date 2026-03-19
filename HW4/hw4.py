import pandas as pd
stk = "TSLA.csv.xlsx"
data = pd.read_excel(stk)
print(data)