from __future__ import (absolute_import, division, print_function,unicode_literals)
import backtrader as bt
import backtrader.feeds as btfeeds
from datetime import date  # date and time functionality
# from MLstrategy import MLstrategy as st
# from SimpleStrategy import SimpleStrategy as st
from OneCandlPredict_Strategy import OneCandlPredict_Strategy as st
import yfinance as yf
import backtrader.feeds
import datetime
from GetData import GetData



class BackTesting():

    def __init__(self):
        # print('BackTesting.ticker', st.ticker)

        ticker = 'SPY'
        period = "1d"
        interval = "1m"
        endDate = date(2021, 6, 5)
        startDate = date(2021, 6, 3)
        tikerData = GetData(ticker, startDate, endDate)

        self.data = btfeeds.GenericCSVData(
            dataname='filename.csv',
            timeframe=bt.TimeFrame.Minutes,
            compression=1,
            sessionstart=datetime.time(9, 30),
            sessionend=datetime.time(16, 0),
            nullvalue=0.0,
            dtformat=('%Y-%m-%d %H:%M:%S%z'),
            tmformat=-1,
            time=-1,
            Datetime=0,
            Open=1,
            High=2,
            Low=3,
            Close=4,
            Volume=5,
            openinterest=-1
        )


    def run(self):

        cerebro = bt.Cerebro(stdstats=False)
        cerebro.addobserver(bt.observers.BuySell)

        cerebro.broker.setcash(50000.0)
        # Set the commission - 0.1% ... divide by 100 to remove the %
        cerebro.broker.setcommission(commission=0.001)

        print('add strategy')
        cerebro.addstrategy(st)

        print('add data')
        cerebro.adddata(self.data)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.plot(style='bar', volume=False)