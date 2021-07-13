import backtrader as bt
from PreProcessing import PreProcessing
from GetData import GetData
from model_LSTM import model_LSTM


class StrategyCandlPredict(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (self.barCount, txt))


    def __init__(self):
        # print('StrategyCandlPredict')

        # Keep a reference to the "close" line in the data[0] dataseries

        self.dataClose = self.datas[0].close
        self.dataOpen = self.datas[0].open
        self.dateTime = self.datas[0].datetime


        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.barCount = -1

        tikerData = GetData()
        preProcessing = PreProcessing(tikerData.price)
        dataFrame = preProcessing.creatDataFrame()
        # self.model = model_LSTM(dataFrame, 0.9)
        self.startTesting = len(dataFrame)*0.9

        self.price = tikerData.price


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

        # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %(trade.pnl, trade.pnlcomm))


    def next(self):
        self.barCount = self.barCount + 1




        # print(self.barCount, " ======== ", self.dataClose[0],"-----", self.price['Close'][self.barCount])
        # Check if handeling a test or train candel? Just backtest test candels
        if self.barCount<self.startTesting or self.barCount > len(self.price)-2:
            # self.log('no trade, %d' % self.barCount)
            return

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # print(self.barCount, "open: ", self.price['Open'][self.barCount + 1])
        # print(self.barCount, "clos: ", self.price['Close'][self.barCount + 1])
        # print(self.barCount, "high: ", self.price['High'][self.barCount + 1])
        # print(self.barCount, " low: ", self.price['Low'][self.barCount + 1])
        # print("close ======== ", self.dataClose[0])

        # nStock = int(self.getvalue()/self.price['High'][self.barCount + 1])
        print("getsizer ======== ", self.order_target_size())
        nStock = 1

        self.order = self.buy(exectype=bt.Order.Limit,price=self.price['Low'][self.barCount+1], size=nStock)
        print(self.barCount, " ======================buy at: ", self.price['Low'][self.barCount+1])

        self.order = self.sell(exectype=bt.Order.Limit, price=self.price['High'][self.barCount + 1], size=nStock)
        print(self.barCount, "----------------------------------sell at: ", self.price['High'][self.barCount + 1])


    # def next(self):
    #     self.barCount = self.barCount + 1
    #
    #
    #     # print(self.barCount, " ======== ", self.dataClose[0],"-----", self.price['Close'][self.barCount])
    #     # Check if handeling a test or train candel? Just backtest test candels
    #     if self.barCount<self.startTesting or self.barCount > len(self.price)-1:
    #         # self.log('no trade, %d' % self.barCount)
    #         return
    #
    #     # Check if an order is pending ... if yes, we cannot send a 2nd one
    #     if self.order:
    #         return
    #
    #     # nextPrice = self.model.predictNextCand(self.barCount)
    #     # nextPrice = self.price['Close'][self.barCount]
    #     # print(self.price['Open'][self.barCount], " ===============", self.price['Close'][self.barCount])
    #
    #     # Not yet ... we MIGHT BUY if ...
    #     # if self.dataClose[0] < nextPrice:
    #     # if 1 < 2:
    #     if self.price['Open'][self.barCount] < self.price['Close'][self.barCount]:
    #
    #         # print('currentPrice: ', self.dataclose[0], 'nextPrice: ', nextPrice)
    #
    #         # BUY, BUY, BUY!!! (with default parameters)
    #
    #         # self.log('BUY CREATE, %.2f' % self.dataclose[0]*0.99)
    #
    #
    #         # Keep track of the created order to avoid a 2nd order
    #         #valid=datetime.datetime.now() + datetime.timedelta(days=3))
    #         # self.order = self.buy(price=self.dataOpen[0])
    #         self.order = self.buy(exectype=bt.Order.Limit,price=self.price['Open'][self.barCount]+1)
    #         print(self.barCount, " ======================buy at: ", self.price['Open'][self.barCount]+1)
    #
    #         # print(self.barCount, "open: ", self.price['Open'][self.barCount + 1])
    #         # print(self.barCount, "clos: ", self.price['Close'][self.barCount + 1])
    #         # print(self.barCount, "high: ", self.price['High'][self.barCount + 1])
    #         # print(self.barCount, " low: ", self.price['Low'][self.barCount + 1])
    #         # print("close ======== ", self.dataClose[0])
    #
    #     # Check if we are in the market
    #     if self.position:
    #
    #         # SELL, SELL, SELL!!! (with all possible default parameters)
    #         # self.log('SELL CREATE, %.2f' % nextPrice)
    #
    #         # Keep track of the created order to avoid a 2nd order
    #         # self.order = self.sell(price=self.dataClose[0])
    #         self.order = self.sell(exectype=bt.Order.Limit, price=self.price['Close'][self.barCount]+1)
    #         print(self.barCount, "----------------------------------sell at: ", self.price['Close'][self.barCount]+1)
