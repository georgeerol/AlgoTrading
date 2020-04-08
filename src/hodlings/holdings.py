import robin_stocks as rh
import pandas as pd
from datetime import datetime
import numpy as np
import json

# logging
content = open('config.json').read()
config = json.loads(content)
rh.login(config['username'], config['password'], by_sms=False)

# Get available stocks and store them into a Panda DataFrame
my_stocks = rh.build_holdings()
df = pd.DataFrame(my_stocks)
df = df.T
df['ticker'] = df.index
df = df.reset_index(drop=True)
cols = df.columns.drop(['id', 'type', 'name', 'pe_ratio', 'ticker'])
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')

# Save as csv
df.to_csv('stocks.csv')
