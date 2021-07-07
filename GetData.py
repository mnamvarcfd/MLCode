from pandas_datareader.data import DataReader
import yfinance as yf
import mplfinance as mpf
from datetime import date


class GetData:

    def __init__(self, ticker, startDate, endDate, interval):
        self.pricSourc = 'yahoo'
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.interval = interval

        # self.price = DataReader(self.ticker, self.pricSourc, self.startDate, self.endDate)
        self.price = yf.download(ticker, start=startDate, end=endDate, interval=interval, auto_adjust=True)

        self.priceFileName = 'priceData.csv'


    def __init__(self):
        self.pricSourc = 'yahoo'
        self.ticker = 'MSFT'
        self.startDate = date(2021, 6, 20)
        self.endDate = date(2021, 7, 2)
        self.interval = "15m"

        # self.price = DataReader(self.ticker, self.pricSourc, self.startDate, self.endDate)
        self.price = yf.download(self.ticker, start=self.startDate, end=self.endDate, interval=self.interval, auto_adjust=True)

        self.priceFileName = 'priceData.csv'

    def writePric(self):
        self.price.to_csv(self.priceFileName)
        # self.price.reset_index(inplace=True, drop=False)
        # price.index = pd.DatetimeIndex(price['Datetime'])


    def plotCandleStick(self):
        self.price.index.name = 'Date'
        mpf.plot(self.price, title=self.ticker, type='candle')


    def getPrice(self):
        return self.price