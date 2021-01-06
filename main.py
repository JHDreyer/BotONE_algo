import requests
import pandas as pd
import json

number_of_elements = 10
response = requests.get(f"https://www.bitmex.com/api/v1/quote/bucketed?binSize=1m&partial=false&symbol=XBT&count={number_of_elements}&reverse=false&startTime=2020-12-22&endTime=2020-12-22")

initial_data = response.json()

df = pd.DataFrame([initial_data[i].values() for i in range(number_of_elements)],columns=['timestamp','symbol', 'bidSize', 'bidPrice', 'askPrice', 'askSize'])
df = df.drop(columns=['symbol'])
df = df.set_index(['timestamp'])

print(df['bidSize']-df['askSize'])

#df = pd.DataFrame(removed_column_data, columns = ['Timestamp', 'bidSize','bidPrice','askPrice','askSize'])
#print(df.head())
#https://www.bitmex.com/api/v1/quote?symbol=XBT&count=100&reverse=false
#https://www.bitmex.com/api/v1/quote?symbol=XBT:daily&count=100&reverse=false&startTime=2020-01&endTime=2020-05

