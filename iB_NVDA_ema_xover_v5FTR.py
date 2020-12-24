"""
    Title: NVDA 200-103-20 30 mins EMA crossover 
    Description: This is a long only strategy which buys on EMA20 
    crossover EMA103 if close is already above EMA200; The position is 
    closed based on EMA20 crossunder EMA103 or through stoplosses.
    
    Asset class: Equities
    Dataset: NYSE Minute

    Current LOG / Objective:
    Have iBridgePy_bot notify me on Telegram

"""
from my_ibridgepy_tools import no_power_alert, do_work_scheduler

def initialize(context):
    context.security = symbol('NVDA')
    context.params = {'pcsl':1-1.4*0.01,    # Previous Close SL
                      'bpsl':1-5*0.01,      # Buy Price SL
                      'ocsl':1-1.2*0.01,    # Open/Close SL
                      'longTrailPerc':3*0.01,       # Trailing SL 
                      'longStopPrice':0.0,
                      'ep':0.0              # Variable for recording a position's entry price
                      }
    
    #signalling whether no power telegram has already been sent
    context.battery_flags = {99:0,90:0,80:0,70:0,60:0,55:0,54:0,53:0,52:0,51:0,50:0,40:0,30:0,20:0,10:0}                         
       
         
def handle_data(context, data):
    # home-server has power?
    no_power_alert(context)
    
    # sTime is the IB server time. 
    sTime = get_datetime()
    
    # Is it time? (:29 or :59 mins on the hour)
    if do_work_scheduler(sTime) == True:
        do_work(context, data)
            

def do_work(context, data):
    
    # fetch enough historical data to calculate EMAs
    hist = request_historical_data(context.security, '30 mins', '16 D')
    
    # EMAs calculation
    hist['ema_20'] = hist['close'].ewm(span=20, adjust=False).mean()
    hist['ema_103'] = hist['close'].ewm(span=103, adjust=False).mean()
    hist['ema_200'] = hist['close'].ewm(span=200, adjust=False).mean()
    
    
    # Trailing Stoploss level calculation
    # if count_positions(context.security) > 0:
    #     stopValue = hist['close'][-1] * (1 - context.params['longTrailPerc'])
    #     context.params['longStopPrice'] = max(stopValue, context.params['longStopPrice'])
    # else:
    #     context.params['longStopPrice'] = 0
    
    
    if count_positions(context.security) != 0:
        if hist['close'][-1] > hist['ema_200'][-1] and hist['ema_20'][-1] > hist['ema_103'][-1] and hist['ema_20'][-2] <= hist['ema_103'][-1]:
            print(hist.index[-1], 'BUY! BUY! BUY!')
            orderId = order_target_percent(context.security, 0.01)
            order_status_monitor(orderId, target_status=['Filled', 'Submitted', 'PreSubmitted', 'PendingSubmit'], waitingTimeInSecond=300)
            context.params['ep'] = hist['close'][-1]
            # context.params['longStopPrice'] = hist['close'][-1]
            
    else:
        if hist['close'][-1] < hist['ema_103'][-1]:
            # close trade
            print(hist.index[-1], 'close<Long_EMA')
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status=['Filled', 'Submitted', 'PreSubmitted', 'PendingSubmit'], waitingTimeInSecond=300)
            
        elif hist['close'][-1] < hist['close'][-2] * context.params['pcsl']:
            # close trade
            print(hist.index[-1], 'PCSL sell')
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status=['Filled', 'Submitted', 'PreSubmitted', 'PendingSubmit'], waitingTimeInSecond=300)
            
        elif hist['close'][-1] < context.params['ep'] * context.params['bpsl']:
            # close trade
            print(hist.index[-1], 'BPSL sell')
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status=['Filled', 'Submitted', 'PreSubmitted', 'PendingSubmit'], waitingTimeInSecond=300)
        
        elif hist['close'][-1] < hist['open'][-1] * context.params['ocsl']:
            # close trade
            print(hist.index[-1], 'OCSL sell')
            orderId = order_target_percent(context.security, 0.0)
            order_status_monitor(orderId, target_status=['Filled', 'Submitted', 'PreSubmitted', 'PendingSubmit'], waitingTimeInSecond=300)
        
        # elif hist['close'][-1] < context.params['longStopPrice']:
        #     # close trade
        #     print(hist.index[-1], 'TSL sell')
        #     context.flag = 0
            # orderId = order_target_percent(context.security, 0.0)
            # order_status_monitor(orderId, target_status=['Filled', 'Submitted', 'PreSubmitted', 'PendingSubmit'], waitingTimeInSecond=300)
            
        else:
            pass