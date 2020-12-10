# NVDA_EMAs_crossover
Trading algorithm that places long positions when price is above the baseline EMA and the fast EMA crosses over the slow EMA. Position exits on a series of stoploss indicators.

![](images/README_header.jpg)


This is my own very first project in Python and for algorithmic trading. I begun this project for fun, after I begun seriously guessing price rises for a few stock tickers of my liking with informed decisions mostly based on personal intuition and sentiment analysis done by myself. I quickly realized that:
<ul>
  <li>Though successful (9% monthly returns), my performance was as good as my daily time commitment and analysis to preparing for market open</li>
  <li>90% of my losses where due to FOMO or the hope that a losing trade would bounce back</li>
</ul>

And so I wondered whether there could be a way to automate entering and exiting trades through a predetermined strategy, removing so also the major cause of money loss, i.e. the human fear factor.

I first came across with TradingView.com and its own programming language. I experimented for a while, studying the fundamentals of technical analysis until I realized that if I wanted to insightfully find out the most effective technical indicator/s, their best parameters levels and combinations tha would produce the best trading strategies with the most consistent high positive returns and the lowest drawdowns, I had to tab the different results of each combination in excel. 

Said and masochistically done it, I begun a manual forward test on eToro.com paper account. Yippie!!! Finally the model will make me rich!! ..or so I though! Though the model with the best overfit and then normalized strategy was making money on Tradingview.com, the reality is that by the time that I: a) received the notifications on my phone; b) saw them; c) took action, the momentum , if not the trade, was already over, and eToro being eToro, their very large spread did not allowed for the gains I was seeing on TradingView.com (note: TradingView does not allow for directly trading a strategy with a connected broker, though they now have some escamotage to achieve this result).

So, back to the drawing table, the main issue now was still the human factor, i.e. my responsiveness to the signals, and the large bid/offer spread I had to overcome each time I placed a trade.

Looking around on the net I discovered that InteractiveBrokers was one of the main routes to implement algorithmic trading and so I studied their API, learnt Python and iBridgePy from scratch and now I forward test and improve this algo both through their API as well as through Blueshift (Quantopian just closed) with Alpaca and FXCM.

# Strategy returns
<code>(TBC)</code>
