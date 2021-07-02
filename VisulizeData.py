import mplfinance as mpf

class VisulizeData:

    def __init__(self, tikerData):
        self.tikerData = tikerData
        self.pricData = tikerData.price

    def __init__(self, tikerData, dataSet):
        self.tikerData = tikerData
        self.pricData = tikerData.price
        self.dataSet = dataSet




    def plotCandleStick(self):
        self.pricData.index.name = 'Date'
        self.pricData.shape
        mpf.plot(self.pricData, title=self.tikerData.ticker, type='candle')


    def plotCandlePlus(self, additionalData):

        additional = self.dataSet[additionalData]
        apdict = mpf.make_addplot(additional)
        mpf.plot(self.pricData, title=self.tikerData.ticker, type='candle',addplot=apdict)










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

