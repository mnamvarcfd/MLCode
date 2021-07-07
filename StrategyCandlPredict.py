import backtrader as bt
from model_LSTM import model_LSTM
from PreProcessing import PreProcessing
from GetData import GetData


class StrategyCandlPredict(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (self.barCount, txt))


    def __init__(self):
        print('StrategyCandlPredict')

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.barCount = 0

        # from GetData import GetData
        # from datetime import date
        # ticker = 'MSFT'
        # interval = "15m"
        # endDate = date(2021, 7, 2)
        # startDate = date(2021, 6, 20)
        # tikerData = GetData(ticker, startDate, endDate, interval)
        tikerData = GetData()
        price = tikerData.price

        # price = self.data.lines

        # price= {}
        # price['Date'] = []
        # price['Open'] = []
        # price['Close'] = []
        # price['High'] = []
        # price['Low'] = []
        # price['Volume'] = []
        #
        # for i in range(0, len(self.data.lines.datetime.array)):
        #     price['Date'].append(self.data.lines.datetime[i])
        #     price['Open'].append(self.data.lines.open[i])
        #     price['Close'].append(self.data.lines.close[i])
        #     price['High'].append(self.data.lines.high[i])
        #     price['Low'].append(self.data.lines.low[i])
        #     price['Volume'].append(self.data.lines.volume[i])

        # price = ['Date', 'Open', 'Close', 'High', 'Low', 'Volume']
        price['Date'] = self.data.lines.datetime[0]
        price['Open'] = self.data.lines.open[0]
        price['Close'] = self.data.lines.close[0]
        price['High'] = self.data.lines.high[0]
        price['Low'] = self.data.lines.low[0]
        price['Volume'] = self.data.lines.volume[0]

        preProcessing = PreProcessing(price)
        dataset = preProcessing.creatDataFrame()
        self.model = model_LSTM(dataset, 0.3)

        self.startTesting = len(dataset)*0.3


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %(trade.pnl, trade.pnlcomm))


    def next(self):
        self.barCount=self.barCount+1

        # Check if handeling a test or train candel? Just backtest test candels
        if self.barCount<self.startTesting:
            # self.log('no trade, %d' % self.barCount)
            return

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        nextPrice = self.model.predictNextCand(self.barCount)

        # Not yet ... we MIGHT BUY if ...
        if self.dataclose[0] < nextPrice:
            print('currentPrice: ', self.dataclose[0], 'nextPrice: ', nextPrice)

            # BUY, BUY, BUY!!! (with default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()

        # Check if we are in the market
        if self.position:

            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('SELL CREATE, %.2f' % nextPrice)

            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell() #exectype=bt.Order.Close