import pandas as pd
import matplotlib.pyplot as plt
from indicators import dpo, vi, ma
import numpy as np


def calculate_buy_or_sell_position(df):

    # Results from experimental testing of parameters
    # parameters crypto: 3,5,200,600,40,180 (1 minute)

    # experimental parameters 210, 5, 100, 400, 40, 150

    # using distribution: ma_op 125;

    ma_par = 125 # was 3 higher number decreases the return but decreases the number of trades # 12
    
    dpo_par_1 = 5 
    dpo_par_2 = 200 # 50 ..504 is the new parameter and only one dpo is used see optimisation
    #dpo_par_3 = 600

    vi_par_1 = 10 # 40
    vi_par_2 = 570 # 150

    """Find a way to optimise the first parameter with the second, second parameters 
    only optimised for the static first parameter"""

    df_ma = ma(ma_par, df)

    df['buySell_ma'] = np.where(df['close'].astype(float) > df_ma['ma'].astype(float), 5000, -5000)
 
    df_dpo = dpo(dpo_par_1, df)
    df['DPO_MA1'] = df_dpo['DPO'].rolling(window=dpo_par_2, min_periods=0).mean()
    #df['DPO_MA2'] = df_dpo['DPO'].rolling(window=dpo_par_3, min_periods=0).mean()  # was 420
    #df['buySell_DPO'] = np.where(df['DPO_MA1'] > df['DPO_MA2'], 5000, -5000)   
    df['buySell_DPO'] = np.where(df['DPO_MA1'] > 0, 5000, -5000) # this is the new and imporved dpo

    '''if plot == True: 
        plt.plot(df_dpo['DPO'], 'k')
        plt.plot(df['DPO_MA1'], 'b')
        plt.plot(df['DPO_MA2'], 'r')
        #plt.plot(df['close'], 'g')
        plt.show()'''

    df_vi = vi(vi_par_1, df)
    df['VI_MA+'] = df_vi['VI+'].rolling(window=vi_par_2, min_periods=0).mean()  # was 250 both
    df['VI_MA-'] = df_vi['VI-'].rolling(window=vi_par_2, min_periods=0).mean()
    df['buySell_VI'] = np.where(df['VI_MA+'] > df['VI_MA-'], 5000, -5000)

    '''if plot == True:
        plt.plot(df['VI_MA+'])
        plt.plot(df['VI_MA-'])
        plt.show()'''

    print('Compiling all indicators')

    # actual compilation
    """df['buySell'] = np.where(df['buySell_DPO'] & df['buySell_VI'] == 5000, 5000, -5000)
    df['buySell'] = np.where(df['buySell'] & df_ma['buySell_ma'] == 5000, 5000, -5000)"""

    # experimental
    """df['buySell'] = np.where(df['buySell_VI'] & df_ma['buySell_ma'] == 5000, 5000, -5000)
    df_buySell = df"""

    # experimental:
    df['buySell'] = df['buySell_VI']
    #df_buySell = df

    df_buySell = df
    print('Compilation complete')
    return df_buySell

def return_on_indicated_trades(df):

    i = 0
    value_open = 0
    value_close = 0
    df = df.reset_index(drop=True)
    buy_sell = [0]

    # get stock price when a trade is indicated (change in buy/sell recommendation)
    while i < df.index[-1]:
        if df.loc[i + 1, 'buySell'] > df.loc[i, 'buySell']:
            value_open = df.loc[i + 1, 'open']
            # df.loc[i+1, 'trade_buy'] = value_open
        if df.loc[i + 1, 'buySell'] < df.loc[i, 'buySell']:
            value_close = df.loc[i, 'close']
            # df.loc[i, 'trade_sell'] = value_close
        if value_open > 0:
            buy_sell.append(value_open)
        if value_close > 0:
            buy_sell.append((-1) * value_close)

        value_open = 0
        value_close = 0
        i += 1

    buy_sell = pd.Series(buy_sell)
    #print(buy_sell)

    # calculate return on trades (from buy and sell price, buy+ & sell-)
    i = 0
    returns = []

    while i < (buy_sell.size-1):
        if buy_sell[i] > 0 and buy_sell[i + 1] < 0:
            pct = ((buy_sell[i + 1] * (-1) - buy_sell[i]) / buy_sell[i]) * 100
            returns.append(pct)
        i += 1

    returns = pd.Series(returns)
    sumation = returns.sum()
    final_output = {'total_return': sumation, 'total_trades':returns.size}

    return final_output

def optimal_distribution_ma(df):

    distribution_data = pd.DataFrame(columns=['parameter', 'RPT'])

    for counter in range(5,395, 15):
        df_ma = ma(counter, df)

        df['buySell_ma'] = np.where(df['close'].astype(float) > df_ma['ma'].astype(float), 5000, -5000)
        df['buySell'] = df['buySell_ma']

        result = return_on_indicated_trades(df)

        output_df = pd.DataFrame({'parameter':[counter],'RPT': [result['total_return']/result['total_trades']]})
        
        distribution_data = distribution_data.append(output_df)

        print(counter)
    
    distribution_data.to_csv('RPT_distribution_ma.csv')

    df = pd.read_csv("RPT_distribution_ma.csv")
    highest_RPT = max(df['RPT'])
    index_max_parameter = df['RPT'].idxmax()
    print(f"index of max {index_max_parameter}")
    max_parameter = df['parameter'].iloc[index_max_parameter]

    results = {'max_RPT':highest_RPT, 'optimal_parameter':max_parameter}
    return results


def optimal_distribution_dpo(df):

    distribution_data = pd.DataFrame(columns=['parameter', 'RPT'])

    for dpo_par_2 in range(500,510,1):

        dpo_par_1 = 5
        #dpo_par_2 = 240 # 100
        
        df_dpo = dpo(dpo_par_1, df)
        df['DPO_MA1'] = df_dpo['DPO'].rolling(window=dpo_par_2, min_periods=0).mean()
        #df['DPO_MA2'] = df_dpo['DPO'].rolling(window=dpo_par_3, min_periods=0).mean()  # was 420
        #df['buySell_DPO'] = np.where(df['DPO_MA1'] > df['DPO_MA2'], 5000, -5000) experimetal algo follows
        df['buySell_DPO'] = np.where(df['DPO_MA1'] > 0, 5000, -5000)
        df['buySell'] = df['buySell_DPO']

        result = return_on_indicated_trades(df)

        rpt = result['total_return']/result['total_trades']

        #output_df = pd.DataFrame({'parameter_ratio':[dpo_par_3/dpo_par_2],'RPT': [rpt]})
        output_df = pd.DataFrame({'parameter':[dpo_par_2],'RPT': [rpt]})

        distribution_data = distribution_data.append(output_df)

        print(f'{rpt} and {dpo_par_2}')

    distribution_data.to_csv('RPT_distribution_dpo.csv')

    df = pd.read_csv("RPT_distribution_dpo.csv")
    highest_RPT = max(df['RPT'])
    index_max_parameter = df['RPT'].idxmax()
    print(f"index of max {index_max_parameter}")
    max_parameter = df['parameter'].iloc[index_max_parameter]

    results = {'max_RPT':highest_RPT, 'optimal_parameter':max_parameter}
    return results


def optimal_distribution_vi(df):

    distribution_data = pd.DataFrame(columns=['parameter', 'RPT'])

    for vi_par_2 in range(565,575,1):

        vi_par_1 = 10

        df_vi = vi(vi_par_1, df)
        df['VI_MA+'] = df_vi['VI+'].rolling(window=vi_par_2, min_periods=0).mean()  # was 250 both
        df['VI_MA-'] = df_vi['VI-'].rolling(window=vi_par_2, min_periods=0).mean()
        df['buySell_VI'] = np.where(df['VI_MA+'] > df['VI_MA-'], 5000, -5000)
        df['buySell'] = df['buySell_VI']

        result = return_on_indicated_trades(df)

        rpt = result['total_return']/result['total_trades']

        #output_df = pd.DataFrame({'parameter_ratio':[dpo_par_3/dpo_par_2],'RPT': [rpt]})
        output_df = pd.DataFrame({'parameter':[vi_par_2],'RPT': [rpt]})

        distribution_data = distribution_data.append(output_df)

        print(f'{rpt} and {vi_par_2}')

    distribution_data.to_csv('RPT_distribution_vi.csv')

    df = pd.read_csv("RPT_distribution_vi.csv")
    highest_RPT = max(df['RPT'])
    index_max_parameter = df['RPT'].idxmax()
    print(f"index of max {index_max_parameter}")
    max_parameter = df['parameter'].iloc[index_max_parameter]

    results = {'max_RPT':highest_RPT, 'optimal_parameter':max_parameter}
    return results

def back_test_buy(df):

    df = calculate_buy_or_sell_position(df)
    datapoints = int(df['close'].size)

    i = 0
    value_open = 0
    value_close = 0
    df = df.reset_index(drop=True)
    buy_sell = [0]

    # get stock price when a trade is indicated (change in buy/sell recommendation)
    while i < df.index[-1]:
        if df.loc[i + 1, 'buySell'] > df.loc[i, 'buySell']:
            value_open = df.loc[i + 1, 'open']
            # df.loc[i+1, 'trade_buy'] = value_open
        if df.loc[i + 1, 'buySell'] < df.loc[i, 'buySell']:
            value_close = df.loc[i, 'close']
            # df.loc[i, 'trade_sell'] = value_close
        if value_open > 0:
            buy_sell.append(value_open)
        if value_close > 0:
            buy_sell.append((-1) * value_close)

        value_open = 0
        value_close = 0
        i += 1

    buy_sell = pd.Series(buy_sell)
    print(buy_sell)

    # calculate return on trades (from buy and sell price, buy+ & sell-)
    i = 0
    returns = []

    while i < (buy_sell.size-1):
        if buy_sell[i] > 0 and buy_sell[i + 1] < 0:
            pct = ((buy_sell[i + 1] * (-1) - buy_sell[i]) / buy_sell[i]) * 100
            returns.append(pct)
        i += 1

    returns = pd.Series(returns)
    sumation = returns.sum()

    print(f'The  simple return is: {sumation}\n')
    print(f'The total trades: {int(returns.size)}\n')
    print(f"The total timeperiods: {datapoints} ")
    print(f"The return per timeperiod is {sumation/(df['close'].size)}%")

    plt.title('Returns based on the backtest')
    plt.xlabel(f'Number of trades (Over {round(datapoints/1440)} Days) ')
    plt.ylabel(f'% Profit per trade ') #(Sum = {round(sum)}%)
    plt.fill_between(returns.index, returns, color='green')
    plt.axhline(color='black')
    plt.show()
    return