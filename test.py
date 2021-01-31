#from runner import trade_buySell_Binance
from backtest import back_test_buy, optimal_distribution_ma, optimal_distribution_dpo, optimal_distribution_vi
import pandas as pd
from binance_API import current_position, market_price_order, get_1min_ohlc_df_binance
from bitmex_API import current_postion_bitmex,bitmex_quote,market_price_order_bitmex
from runner import trade_buySell_Bitmex
from math import floor

#trade_buySell_Bitmex('XBTUSD', 'BTCUSDT', 297)
"""position = current_postion_bitmex('XBTUSD')
print(position)"""
#bitmex_quote("XBTUSD")
#current_postion_bitmex('XBTUSD')
#df = get_1min_ohlc_df_binance('BTCUSDT', 21)
#df.to_csv('Testdata.csv')

df = pd.read_csv('Testdata.csv')
back_test_buy(df)

#output = optimal_distribution_vi(df)
#print(output)
#back_test_buy(df)





"""df = pd.read_csv('BTCUSDT_1min_ohlc_data.csv')

print(df.head())
print(df.tail())
df = df.iloc[-600:]
print(df.size)
print(df.head())
print(df.tail())"""

"""df = get_1min_ohlc_df_binance('BTCUSDT', 1)

df['close'] = pd.to_numeric(df['close'])
df['high'] = pd.to_numeric(df['high'])
df['low'] = pd.to_numeric(df['low'])
df['open'] = pd.to_numeric(df['open'])

print(df.head())
print(df.tail())

back_test_buy(df)"""

#back_test_buy(df)venv\
