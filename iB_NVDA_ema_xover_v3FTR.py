
"""
    Title: NVDA 200-103-20 30 mins EMA crossover 
    Description: This is a long only strategy which buys on EMA20 
    crossover EMA103 if close is already above EMA200; The position is 
    closed based on EMA20 crossunder EMA103 or through stoplosses.
    
    Asset class: Equities
    
    Last LOG:
    Added Trailing Stoploss logic
    
    To run live this script, comment all context.flag and uncomment the order placements
    Note: this strategy is still nor viable for live deployment as the conditions 
    are met several time within a single candle because they are checked every minute
    Next improvement: have the script execute only every 30 minutes
"""

def initialize(context):
    context.flag = False
    context.security = symbol('NVDA')
    context.params = {'pcsl':1-1.4*0.01,    # Previous Close SL
                      'bpsl':1-5*0.01,      # Buy Price SL
                      'ocsl':1-1.2*0.01,    # Open/Close SL
                      'longTrailPerc':3*0.01,       # Trailing SL %
                      'longStopPrice':0.0,
                      'ep':0.0              # Variable for recording a position's entry price
                      }
    context.flag = 0
           
     
def handle_data(context, data):
    # fetch enough historical data to calculate EMAs
    hist = request_historical_data(context.security, '30 mins', '30 D')
    
    hist['ema_20'] = hist['close'].ewm(span=20, adjust=False).mean()
    hist['ema_103'] = hist['close'].ewm(span=103, adjust=False).mean()
    hist['ema_200'] = hist['close'].ewm(span=200, adjust=False).mean()
    
    
    # if count_positions(context.security) > 0:
    if context.flag > 0:
        stopValue = hist['close'][-1] * (1 - context.params['longTrailPerc'])
        context.params['longStopPrice'] = max(stopValue, context.params['longStopPrice'])
    else:
        context.params['longStopPrice'] = 0
        
        
    # if count_positions(context.security) == 0:
    if context.flag == 0:
        if hist['close'][-1] > hist['ema_200'][-1] and hist['ema_20'][-1] > hist['ema_103'][-1] and hist['ema_20'][-2] <= hist['ema_103'][-1]:
            print(hist.index[-1], 'BUY! BUY! BUY!')
            # orderId = order_target_percent(context.security, 0.01)
            # order_status_monitor(orderId, target_status='Filled')
            context.flag = 1
            context.params['ep'] = hist['close'][-1]
            context.params['longStopPrice'] = hist['close'][-1]
                        
    else:
        # print(context.params['longStopPrice'])
        if hist['close'][-1] < hist['ema_103'][-1]:
            # close trade
            print(hist.index[-1], 'close<Long_EMA')
            context.flag = 0
            # orderId = order_target_percent(context.security, 0.0)
            # order_status_monitor(orderId, target_status='Filled')
            
        elif hist['close'][-1] < hist['close'][-2] * context.params['pcsl']:
            # close trade
            print(hist.index[-1], 'PCSL sell')
            context.flag = 0
            # orderId = order_target_percent(context.security, 0.0)
            # order_status_monitor(orderId, target_status='Filled')
            
        elif hist['close'][-1] < context.params['ep'] * context.params['bpsl']:
            # close trade
            print(hist.index[-1], 'BPSL sell')
            context.flag = 0
            # orderId = order_target_percent(context.security, 0.0)
            # order_status_monitor(orderId, target_status='Filled')
        
        elif hist['close'][-1] < hist['open'][-1] * context.params['ocsl']:
            # close trade
            print(hist.index[-1], 'OCSL sell')
            context.flag = 0
            # orderId = order_target_percent(context.security, 0.0)
            # order_status_monitor(orderId, target_status='Filled')
        
        elif hist['close'][-1] < context.params['longStopPrice']:
            # close trade
            print(hist.index[-1], 'TSL sell')
            context.flag = 0
            # orderId = order_target_percent(context.security, 0.0)
            # order_status_monitor(orderId, target_status='Filled')
            
        else:
            pass
