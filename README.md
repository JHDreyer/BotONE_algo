# Trading bot with Binance & BitMEX

Jargon summary:
* API - Application programmable interface (a web platform's interface with code that can be used to access different features)
* API keys - Strings that act as authentication when a reguest is posted to a website
* API Client - the entity (owner of the API keys) that is authenticated for each API request
* OHLC data - open, high, low, close data for a particular coin, token or intrument
* Long or short position - buy position and a sell position, respectively
* Dataframe - a pandas library datastructure similar to an Excel sheet or table with rows and columns


## Components of the project:

* runner.py is the file with the function for the excecution of the main script
* binance_API.py and bitmex_API.py contain the API keys, setup of the Client, and functions that evelop functional blocks of API requests that return useful data or make changes to the Client's positions (trades)
* indicators.py contains the functions,that return a pandas dataframes, of the technical indicators used to make predictions
* backtest.py contains functions that process the financial data and technical indicator values together to make a prediction of the ideal position for the Client (long or short position) and returns the data in dataframe form
* logic - if statements

### Flow of the programme (High level overview):

1. The function trade_buy_sell_Binance/BitMEX() in runner.py runs every second and checks if a minute of time has passed (when the time changes by a minute)
2. If a minute has passed, new financial data is available an pulled by the trade_buy_sell_Binance/BitMEX()  using the functions in bitmex/binance_API.py
3. This data is fed to the calculate_buy_or_sell_position() function in backtest.py that runs the data through the specified technical indicators that are located in indicators.py. The function then also compares indicators to preset threshold values (an integer) to determine if an indicator indicates a long or short position. Indicators can then be complied in different combinations for different prediction models. 
4. The returned dataframe from calculate_buy_or_sell_position() contains information that dicates a long/short position that is extracted with logic and the appropiate API call is make using the functions defined in bitmex/binance_API.py

Note: 2 runner functions exist, Binance and BitMEX are seperate (trade_buy_sell_Binance/BitMEX())

runner.py(trade_buy_sell_Binance/Bitmex) -> backtest.py(calculate_buy_or_sell_position()) 
-> bitmex/binance_API.py (financial data pulled) -> backtest.py(calculate_buy_or_sell_position()) -> inicators.py (indicator values generated) -> 
backtest.py(calculate_buy_or_sell_position()) (long/short position determined) 
-> runner.py -> bitmex/binance_API.py -> Client position atlered

### Logic in runner.py:

Example:
* When calculate_buy_or_sell_position() speficies a long position, the function first checks what the Client's current position.
* When the position is short, the position is reversed. If it is long the position will remain unchanged.
* The current position is always checked and then changed or unchanged depending on the prediction of the data pulled from backtest.py.
