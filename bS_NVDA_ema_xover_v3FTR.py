"""
    Title: NVDA 200-103-20 30 mins EMA crossover 
    Description: This is a long only strategy which buys on EMA20 
    crossover EMA103 if close is already above EMA200; The position is 
    closed based on EMA20 crossunder EMA103 or through stoplosses.
    
    Asset class: Equities
    Dataset: NYSE Minute

    LOG:
    Added Trailing Stoploss logic
    
    To run live this script, comment all context.flag and uncomment the order placements
    Note: this strategy is still nor viable for live deployment as the conditions 
    are met several time within a single candle because they are checked every minute

    Next improvement: have the script execute only every 30 minutes

"""
# Imports
from zipline.api import symbol, order_target_percent


def initialize(context):
    context.stock = symbol('NVDA')
    context.params = { 'short_ema_span':20,
                       'long_ema_span':103,
                       'baseline_ema_span':200,
                       'pcsl':1-1.4*0.01,    # Previous Close SL
                       'bpsl':1-5*0.01,      # Buy Price SL
                       'ocsl':1-1.2*0.01,    # Open/Close SL
                       'longTrailPerc':3*0.01,       # Trailing SL 
                       'longStopPrice':0.0,
                       'ep':0.0
                       }
    context.flag = 0
    

def handle_data(context,data):

    # Fetch 6000 minutes to resample to 200 30T historical bars for the EMAs calculations
    pre_hist = data.history(context.stock, ['open','close'], 6000, '1m')
    pre_hist = pre_hist.round(2)
    
    # Resample pre_hist to 30 minutes candles in hist
    hist = pre_hist.resample('30Min').agg({'close': 'last', 'open': 'first'})
    hist = hist.dropna()
 
    # Calculate EMAs
    hist['ema_20'] = hist['close'].ewm(span=context.params['short_ema_span'], adjust=False).mean()
    hist['ema_103'] = hist['close'].ewm(span=context.params['long_ema_span'], adjust=False).mean()
    hist['ema_200'] = hist['close'].ewm(span=context.params['baseline_ema_span'], adjust=False).mean()

    # Trailing Stoploss level calculation
    if context.portfolio.positions[context.stock].amount > 0:
        stopValue = hist['close'][-1] * (1 - context.params['longTrailPerc'])
        context.params['longStopPrice'] = max(stopValue, context.params['longStopPrice'])
    else:
        context.params['longStopPrice'] = 0

    # Entry/exit logic
    if context.portfolio.positions[context.stock].amount == 0:
    # if context.flag == 0:
        if hist['close'][-1] > hist['ema_200'][-1] and hist['ema_20'][-1] > hist['ema_103'][-1] and hist['ema_20'][-2] < hist['ema_103'][-1]:
            order_target_percent(context.stock, 1.0)
            context.params['ep'] = hist['close'][-1]
            print(hist.index[-1], 'BUY! BUY! BUY!')
            context.params['longStopPrice'] = hist['close'][-1]
            # context.flag = 1

    else:
        if hist['close'][-1] < hist['ema_103'][-1] and hist['close'][-2] >= hist['ema_103'][-1]:
            order_target_percent(context.stock, 0.0)
            print(hist.index[-1], 'close<Long_EMA')
            # context.flag = 0

        elif hist['close'][-1] < hist['close'][-2] * context.params['pcsl']:
            order_target_percent(context.stock, 0.0)
            print(hist.index[-1], 'PCSL sell')
            # context.flag = 0

        elif hist['close'][-1] < context.params['ep'] * context.params['bpsl'] and hist['close'][-2] >= context.params['ep'] * context.params['bpsl']:
            order_target_percent(context.stock, 0.0)
            print(hist.index[-1], 'BPSL sell')
            # context.flag = 0

        elif hist['close'][-1] < hist['open'][-1] * context.params['ocsl']:
            order_target_percent(context.stock, 0.0)
            print(hist.index[-1], 'OCSL sell')
            # context.flag = 0

        elif hist['close'][-1] < context.params['longStopPrice']:
            order_target_percent(context.stock, 0.0)
            print(hist.index[-1], 'TSL sell')
            # context.flag = 0
        else:
            pass
