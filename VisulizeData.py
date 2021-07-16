import mplfinance as mpf
import pandas as pd

class VisulizeData:

    def __init__(self, tiker, dataSet):
        self.tiker = tiker
        self.dataSet = dataSet


    def plotCandleStick(self):
        self.dataSet.index.name = 'Date'
        mpf.plot(self.dataSet, title=self.tiker, type='candle')


    def plotCandlePlus(self, predicted):

        nFutur = len(predicted)
        lendData = len(self.dataSet)
        additionalData = self.dataSet['Close'].copy()

        for i in range(0, nFutur):
            additionalData[lendData - nFutur + i] = predicted[i]

        apdict = mpf.make_addplot(additionalData)
        mpf.plot(self.dataSet, title=self.tiker, type='candle', addplot=apdict)




    def plotCandlePredictData(self, predicted):

        nFutur = len(predicted)
        lendData = len(self.dataSet)
        for i in range(0, nFutur):
            idx = self.dataSet.tail(1).index[0] + pd.Timedelta(minutes=1)
            self.dataSet.loc[idx] = self.dataSet['Close'][-1].copy()

        additionalData = self.dataSet['Close'].copy()

        # result.index.name = 'Date'
        for i in range(0, nFutur):
            additionalData[lendData + i] = predicted[i]

        apdict = mpf.make_addplot(additionalData)
        mpf.plot(self.dataSet, title=self.tiker, type='candle', addplot=apdict)




class VisulizeDataCandle:

    def __init__(self, tikerData):
        self.tikerData = tikerData
        self.pricData = tikerData.price


    def plotCandleStick(self):
        self.pricData.index.name = 'Date'
        self.pricData.shape
        mpf.plot(self.pricData, title=self.tikerData.ticker, type='candle')


    def plotCandlePlus(self, desiredData):
        apdict = mpf.make_addplot(self.pricData[desiredData])
        mpf.plot(self.pricData, title=self.tikerData.ticker, type='candle',addplot=apdict)

