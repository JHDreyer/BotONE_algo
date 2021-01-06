import bitmex
import time, requests, json


# Details are for Testnet profile
bitmex_api_key = "jZTSUxz2azxLYI4xdtVUlsVt"
bitmex_api_secret = "GXD9aIKV75DO7cfWvw8TkDHffMh-e0v1_F-0i3CX1EcZuxr_"
client = bitmex.bitmex()
client = bitmex.bitmex(test = True, api_key=bitmex_api_key, api_secret=bitmex_api_secret)

# 2/3 functions needed placing an order(buy/sell), determining the current position (long/short), 
# the amount of the long or short trade.

def market_price_order_bitmex(symbol_bitmex, quantity, tradeType):

    ordType= 'Market'
    
    if tradeType == 'BUY':
        client.Order.Order_new(symbol=symbol_bitmex, ordType=ordType, orderQty=quantity).result()    
    elif tradeType == 'SELL':
        client.Order.Order_new(symbol=symbol_bitmex, ordType=ordType, orderQty=quantity).result()
    else:
        print('\nError: type of order not specified correctly')

    return # does result show the order placed or shoud it be assigned to a variable and printed?


def current_postion_bitmex(symbol_bitmex):
    positions = client.Position.Position_get().result()
    #filter=json.dumps({"symbol": symbol_bitmex})

    edited = positions[0][0]
    qtyPosition = int(edited['currentQty'])
    print(f'Current quantity:{qtyPosition}')

    # bitmex has a different balance management systetm, no postion is a bitcoin postion, short is a neutral postion. 
    # implement dynamic solution
    if qtyPosition < 0:
        trade_position = 'SHORT'

    elif qtyPosition > 0: # 0 position is a long position without leverage
        trade_position = 'LONG'

    elif qtyPosition == 0:
        trade_position = 'Neutral'
    else:
        print('Error in determining the trading position')

    
    # what should the sign of the quantity be, especially when a long, short position is changed (opposite sign or not?)
    info_position = {'symbol':symbol_bitmex, 'position':trade_position, 'quantity':qtyPosition}
    return info_position

def bitmex_quote(symbol_bitmex):
    result = client.Quote.Quote_get(symbol=symbol_bitmex, reverse=True, count=1).result()
    print(f"The ask price for {symbol_bitmex} is: ${result[0][0]['askPrice']}")
    return