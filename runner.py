from backtest import calculate_buy_or_sell_position
from binance_API import get_1min_ohlc_df_binance, update_data_binance, current_position, market_price_order
# add bitmex function imports here
from bitmex_API import current_postion_bitmex, market_price_order_bitmex
import pandas as pd

from datetime import datetime as dt
import time


def trade_buySell_Binance(ticker_str):

    minute = dt.now().minute
    prev_min = dt.now().minute
    position = 'Unknown'
    # position: should run a check with API (algo should use info to make first trade or not)
    i = 0

    while True:
        if minute == prev_min:
            i += 1

            print(f'{dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")} ({position})')

        if minute != prev_min:
            # the code executed once at the beginning of every new minute
            prev_min = dt.now().minute
            print('\nThe new minute: ' + str(dt.now().minute))
            i = 0

            try:
                # search for existing file to update 

                file = f'{ticker_str}_1min_ohlc_data.csv'
                df = pd.read_csv(file, index_col='timestamp')
                df = update_data_binance(df, ticker_str)
                df.to_csv(f'{ticker_str}_1min_ohlc_data.csv')
                print(f'The existing {ticker_str}.csv was updated')

            except:
                # if try failed, new file is created

                df = get_1min_ohlc_df_binance(ticker_str, 2)
                print(f'The data for {ticker_str} was collected from binance')

            # calculate the buy sell position

            df = pd.read_csv(f'{ticker_str}_1min_ohlc_data.csv', index_col='timestamp')
            df = calculate_buy_or_sell_position(df)

            trade_position = current_position('BTC', 'USDT')

            if df.loc[df.last_valid_index(), 'buySell'] == 5000:
                #  Check for short position cancel it, then buy
                print('The algo said buy')
                if trade_position['position'] == 'SHORT':
                    print(f"Requested buy amount is { trade_position['usdt_ito_btc']}")
                    market_price_order('BTCUSDT', trade_position['usdt_ito_btc'], 'BUY')
                    print('Buy function called')
                    position = 'LONG'
                    # call the function to buy
                else:
                    print('The LONG position remains unchanged')
                    position = 'LONG'

            if df.loc[df.last_valid_index(), 'buySell'] == -5000:
                # check for long position  cancel it, then sell
                print('The algo said sell')
                if trade_position['position'] == 'LONG':
                    # call the sell function
                    print(f"Requested sell amount is {trade_position['btc_balance']}")
                    market_price_order('BTCUSDT', trade_position['btc_balance'], 'SELL')
                    print('Sell function called')
                    position = 'SHORT'
                else:
                    print('The SHORT position remains unchanged')
                    position = 'SHORT'

            print("\n")

        minute = dt.now().minute
        time.sleep(1)

    return

# progression of the steps:
"""
-For loop executes every minute

-Search for file to update or create new file
-Algo calculates what the current position should be
-Actual position is pulled from the platform

-Compares actual position to algo postion 
-Order is executed to make changes to position if they (algo/actual) differ

"""
# copy of edited binance function follows that is edited to work with BitMEX

def trade_buySell_Bitmex(ticker_str_bitmex, ticker_str_binance, trade_amount_usd):

    ticker_str = ticker_str_binance

    minute = dt.now().minute
    prev_min = dt.now().minute
    position = 'Unknown'
    # position: should run a check with API (algo should use info to make first trade or not)
    i = 0

    while True:
        if minute == prev_min:
            i += 1

            print(f'{dt.strftime(dt.now(), "%Y/%m/%d %H:%M:%S")} ({position})')

        if minute != prev_min:
            # the code executed once at the beginning of every new minute
            prev_min = dt.now().minute
            print('\nThe new minute: ' + str(dt.now().minute))
            i = 0

            try:
                # search for existing file to update,
                file = f'{ticker_str}_1min_ohlc_data.csv'
                df = pd.read_csv(file, index_col='timestamp')
                df = update_data_binance(df, ticker_str)
                df.to_csv(f'{ticker_str}_1min_ohlc_data.csv')
                print(f'The existing {ticker_str}.csv was updated')

            except:
                # if try failed, new file is created
                df = get_1min_ohlc_df_binance(ticker_str, 2)
                print(f'The data for {ticker_str} was collected from binance')

            # calculate the buy sell position

            df = pd.read_csv(f'{ticker_str}_1min_ohlc_data.csv', index_col='timestamp')
            df = calculate_buy_or_sell_position(df)

            trade_position = current_postion_bitmex('XBTUSD')

            #  Check for short position cancel it, then buy
            if df.loc[df.last_valid_index(), 'buySell'] == 5000:
                
                print('The algo said buy')

                if trade_position['position'] == 'SHORT':
                    #print(f"Requested buy amount is { trade_position['usdt_ito_btc']}") # bitmex and binance trade position function return different info
                    market_price_order_bitmex('XBTUSD', trade_position['quantity']*-2, 'BUY')
                    print('Buy function called')
                    position = 'LONG'
                    # call the function to buy
                elif trade_position['position'] == 'Neutral':
                    market_price_order_bitmex('XBTUSD', trade_amount_usd, 'BUY')
                    print('Buy function called')
                    position = 'LONG'
                else:
                    print('The LONG position remains unchanged')
                    position = 'LONG'

            # check for long position  cancel it, then sell
            if df.loc[df.last_valid_index(), 'buySell'] == -5000:
                
                print('The algo said sell')

                if trade_position['position'] == 'LONG':
                    # call the sell function
                    #print(f"Requested sell amount is {trade_position['btc_balance']}")
                    market_price_order_bitmex('XBTUSD', trade_amount_usd*-2, 'SELL')
                    print('Sell function called')
                    position = 'SHORT'
                elif trade_position['position'] == 'Neutral':
                    market_price_order_bitmex('XBTUSD', trade_amount_usd*-1, 'SELL')
                    print('Sell function called')
                    position = 'SHORT'
                else:
                    print('The SHORT position remains unchanged')
                    position = 'SHORT'
                
            print("\n")

        minute = dt.now().minute
        time.sleep(1)

    return