# iBridgePy NVDA_ema_xover strategy code

# Imports
# import pandas    
# pandas.set_option('display.max_rows', None)
# pandas.set_option('max_columns', None)
# pandas.set_option('display.width', 320)
# import talib as ta
    

def initialize(context):
    context.flag = False
    context.security = symbol('NVDA')
    context.params = {'pcsl':1-1.4*0.01,    # Previous Close SL
                      'bpsl':1-5*0.01,      # Buy Price SL
                      'ocsl':1-1.2*0.01,    # Open/Close SL
                      'tsl':1-3*0.01,       # Trailing SL 
                      'ep':0.0
                      }
    context.flag = 0
           
     
def handle_data(context, data):
    # fetch enough historical data to calculate EMAs
    hist = request_historical_data(context.security, '30 mins', '45 D')
    
    # print('checkpoin B')
    hist['ema_20'] = hist['close'].ewm(span=20, adjust=False).mean()
    hist['ema_103'] = hist['close'].ewm(span=103, adjust=False).mean()
    hist['ema_200'] = hist['close'].ewm(span=200, adjust=False).mean()
    
    
    # if count_positions(context.security) == 0:
    if context.flag == 0:
        
        if hist['close'][-1] > hist['ema_200'][-1] and hist['ema_20'][-1] > hist['ema_103'][-1] and hist['ema_20'][-2] <= hist['ema_103'][-1]:
            print(hist.index[-1], 'BUY! BUY! BUY!')
            orderId = order_target_percent(context.security, 0.01)
            order_status_monitor(orderId, target_status='Filled')
            context.flag = 1
            context.params['ep'] = hist['close'][-1]
            
    else:
        if hist['close'][-1] < hist['ema_103'][-1]:
            # close trade
            print(hist.index[-1], 'close<Long_EMA')
            context.flag = 0
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status='Filled')
            
        elif hist['close'][-1] < hist['close'][-2] * context.params['pcsl']:
            # close trade
            print(hist.index[-1], 'PCSL sell')
            context.flag = 0
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status='Filled')
            
        elif hist['close'][-1] < context.params['ep'] * context.params['bpsl']:
            # close trade
            print(hist.index[-1], 'BPSL sell')
            context.flag = 0
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status='Filled')
        
        elif hist['close'][-1] < hist['open'][-1] * context.params['ocsl']:
            # close trade
            print(hist.index[-1], 'OCSL sell')
            context.flag = 0
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status='Filled')
        
        elif hist['close'][-1] < hist['close'][-2] * context.params['tsl']:
            # close trade
            print(hist.index[-1], 'TSL sell')
            context.flag = 0
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status='Filled')
            
        else:
            pass
