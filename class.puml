from pandas_datareader.data import DataReader
import yfinance as yf
import pandas as pd
class TikerData:

    def __init__(self, ticker, startDate, endDate):
        self.pricSourc = 'yahoo'
        self.ticker = ticker
        self.startDate = startDate
        self.endDate = endDate
        self.price= self.getPricData()

    def getPricData(self):
        # price = DataReader(self.ticker, self.pricSourc, self.startDate, self.endDate)

        price = yf.download(self.ticker, start=self.startDate, end=self.endDate, interval="1m", auto_adjust=True)

        price.to_csv('filename.csv')
        price.reset_index(inplace=True, drop=False)
        # price.index = pd.DatetimeIndex(price['Datetime'])

        return price

# import yfinance as yf
# intraday_data = yf.download(tickers="BA", period="1d", interval="1m",auto_adjust=True)
# intraday_data.head()
# import matplotlib.pyplot as plt
#
# intraday_data['Close'].plot()
# plt.show()