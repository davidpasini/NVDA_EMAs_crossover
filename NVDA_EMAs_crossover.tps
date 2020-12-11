//@version=4
strategy("EMA(200) + EMA(103) + EMA(20) v.5 LONG Strategy (1 Year)", overlay=true, pyramiding=2, calc_on_every_tick=true, initial_capital=1000, currency=currency.USD, default_qty_type=strategy.cash, default_qty_value=1000)
//strategy("EMA(200) + EMA(103) + EMA(20) v.5 LONG Strategy (1 Year)", overlay=true, calc_on_every_tick=true, initial_capital=1000, currency=currency.USD, default_qty_type=strategy.percent_of_equity, default_qty_value=100)


// === BACKTEST RANGE INPUTS ===
fromDay   = input(defval = 20,    title = "From Day",        type = input.integer, minval = 1, maxval = 31)
fromMonth = input(defval = 5,    title = "From Month",      type = input.integer, minval = 1, maxval = 12)
fromYear  = input(defval = 2019, title = "From Year",       type = input.integer, minval = 1970)
thruDay   = input(defval = 20,    title = "Thru Day",        type = input.integer, minval = 1, maxval = 31)
thruMonth = input(defval = 5,    title = "Thru Month",      type = input.integer, minval = 1, maxval = 12)
thruYear  = input(defval = 2020, title = "Thru Year",       type = input.integer, minval = 1970)

// === BACKTEST RANGE FUNCTION ===
start     = timestamp(fromYear, fromMonth, fromDay, 00, 00)        // backtest start window
finish    = timestamp(thruYear, thruMonth, thruDay, 23, 59)        // backtest finish window
window()  => time >= start and time <= finish ? true : false       // create function "within window of time"


// === EMA INPUTS VALUES TITLE LINE ===
EMAinputvaluesline  = input(defval = true, title = "EMA values  ------------------------------")

// === EMAs INPUTS ===
ma1i = input(20, title="Fast EMA")
ma2i = input(103, title="Medium EMA")
ma3i = input(200, title="Slow EMA")


// === STOPLOSS INPUT VALUES TITLE LINE ===
SLinputvaluesline  = input(defval = true, title = "STOP LOSS values  ----------------------")

// === STOPLOSS INPUTS ===
sli1 = input(title="Previous Close SL (%)", type = input.float, minval=0.0, step=0.1, defval = 1.4) * 0.01
sli2 = input(title="Buy price SL (%)", type = input.float, minval=0.0, step=0.01, defval = 5) * 0.01
sli3 = input(title="Open/Close SL (%)", type = input.float, minval=0.0, step=0.01, defval = 1.2) * 0.01
sl1 = 1 - sli1
sl2 = 1 - sli2
sl3 = 1 - sli3

// Record Entry Buy Price for "Buy price SL" and to trace brackground color during trades
ep = 0.0
ep := na(ep[1]) ? na : ep[1]

// Configure trail stop level with input options (optional)
longTrailPerc = input(title="Trailing SL (%)", type=input.float, minval=0.0, step=0.1, defval=3) * 0.01

// Determine trail stop loss prices
longStopPrice = 0.0

longStopPrice := if (strategy.position_size > 0)
    stopValue = close * (1 - longTrailPerc)
    max(stopValue, longStopPrice[1])
else
    0

plot(series=(strategy.position_size > 0) ? longStopPrice : na, style = plot.style_stepline, color=color.fuchsia)


// === EMAs CALCULATION ===
ma1 = ema(close, ma1i)
ma2 = ema(close, ma2i)
ma3 = ema(close, ma3i)


// === ENTRY AND CLOSE CONDITIONS ===
l_entry()=>close > ma3 and crossover(ma1, ma2)
l_close1()=>crossunder(close, ma2)
l_close2()=>close < close[1] * sl1
l_close3()=>crossunder(close, ep*sl2)
l_close4()=>close < open*sl3


// === BARSSINCE INPUTS VALUES TITLE LINE ===
BSinputvaluesline  = input(defval = true, title = "Bars Since Entry Signal  ------------------------------")

// === EMAs INPUTS ===
bs = input(1, title="Bars since")


// === AVERAGE TRUE RANGE INPUTS TITLE LINE ===
ATRinputvaluesline  = input(defval = true, title = "ATR values  ------------------------------")

// === AVERAGE TRUE RANGE INPUTS ===
atrLen = input(title="ATR Length", type=input.integer, minval=0, step=1, defval=200)
atrThreshold = input(title="ATR Threshold", type = input.float, minval=0.0, step=0.1, defval = 2.0)


// === ENTRY AND CLOSE LOGIC ===
if l_entry() and atr(atrLen) < atrThreshold
    ep := close
    strategy.entry("LE-NVDA-EMA200-103-20-30m", strategy.long, when=window(), comment="LE")

// if barssince(l_entry()) == bs and strategy.position_size > 0
//     strategy.entry("LE-NVDA-EMA200-103-20-30m", strategy.long, qty=5, when=window(), comment="LE-P")

if l_close1()
    strategy.close("LE-NVDA-EMA200-103-20-30m", when=window(), comment="LC")
else 
    if l_close2()
        strategy.close("LE-NVDA-EMA200-103-20-30m", when=window(), comment="LC Previous Close SL")
    else
        if l_close3()
            strategy.close("LE-NVDA-EMA200-103-20-30m", when=window(), comment="LC Buy price SL")
        else
            if l_close4()
                strategy.close("LE-NVDA-EMA200-103-20-30m", when=window(), comment="LC Open/Close SL")
            else
                strategy.exit(id="LE-NVDA-EMA200-103-20-30m", stop=longStopPrice, comment="LC Trailing SL")



// === BACKGROUND COLOR DURING TRADES ===
backgroundColour1 = (strategy.position_size > 0 and close > ep) ? color.green : color.white
bgcolor(color=backgroundColour1, transp=85)
backgroundColour2 = (strategy.position_size > 0 and close < ep) ? color.red : color.white
bgcolor(color=backgroundColour2, transp=85)


// === ENTRY AND CLOSE CONDITIONS ===
plot(ma1, color=#32a852)
plot(ma2, color=#a83232)
plot(ma3, color=#0091ff)
plot(ep, color=#0000ff) 
