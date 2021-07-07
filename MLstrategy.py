import backtrader as bt
from model_LSTM import model_LSTM
from GetData import GetData
from PreProcessing import PreProcessing

# Create a Stratey
class MLstrategy(bt.Strategy):
    params = (
        ('exitbars', 5),
    )

    ticker = 'MSFT'
    period = "1d"
    interval = "1m"
    from datetime import date
    endDate = date(2021, 7, 2)
    startDate = date(2021, 6, 28)


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (self.barCount, txt))



    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        print('tikerData', self.ticker)
        tikerData = GetData(self.ticker, self.startDate, self.endDate)

        preProcessing = PreProcessing(tikerData.price)
        dataset = preProcessing.creatDataSet()
        model = model_LSTM(dataset, 0.3)
        self.model = model
        self.barCount = 0
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
        if self.barCount<self.startTesting:
            # self.log('no trade, %d' % self.barCount)
            return

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        nextPrice = self.model.predict(self.barCount)

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