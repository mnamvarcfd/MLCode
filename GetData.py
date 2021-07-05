from pandas_datareader.data import DataReader
import yfinance as yf
import mplfinance as mpf



class GetData:

    def __init__(self, ticker, startDate, endDate, interval):
        self.pricSourc = 'yahoo'
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.interval = interval

        # self.price = DataReader(self.ticker, self.pricSourc, self.startDate, self.endDate)
        self.price = yf.download(ticker, start=startDate, end=endDate, interval=interval, auto_adjust=True)


    def writePric(self):
        self.price.to_csv('priceData.csv')
        self.price.reset_index(inplace=True, drop=False)
        # price.index = pd.DatetimeIndex(price['Datetime'])


    def plotCandleStick(self):
        self.price.index.name = 'Date'
        mpf.plot(self.price, title=self.ticker, type='candle')