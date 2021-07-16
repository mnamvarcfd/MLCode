# import packages
from datetime import date  # date and time functionality

import numpy as np
from matplotlib import pyplot as plt
# from SMAcross import SMAcross

# ======================input======================
# from mpmath import mpf


# ======================get price data======================

from GetData import GetData
stock = GetData()
# stock.plotCandleStick()
# stock.writePric()


from PreProcessing import PreProcessing
preProcessing = PreProcessing(stock.price)
# dataFrame = preProcessing.creatDataFrame()

dataFrame = preProcessing.creatMultiDataFrame()
# dataFrame['Close'].plot()
# plt.show()


# from model_LSTM import model_LSTM
# model = model_LSTM(dataFrame, 0.7)
# model.predictNextCand(len(dataFrame)-5)
# result = model.predictTrend(len(dataFrame)-500, 500)
# result = np.array(result)
# plt.plot(result)
# plt.show()


# from model_multiInputLSTM import model_multiInputLSTM
# model = model_multiInputLSTM(dataFrame, 0.95)
# iData = len(dataFrame)-10
# predict = model.predictNextCand(len(dataFrame)-10)
# print("predicted Low value: ", predict)



# print("open: ", dataFrame['Open'][len(dataFrame)-10])
# print("clos: ", dataFrame['Close'][len(dataFrame)-10])
# print("high: ", dataFrame['High'][len(dataFrame)-10])
# print(" low: ", dataFrame['Low'][len(dataFrame)-10])

# MSF.plotCandleStick()

# result = model.predictTrend(len(dataFrame)-50, 50)
# result = np.array(result)
# plt.plot(result)
# plt.show()

# for i in range(iData, iData + 10):
#     stock.price['Low'][i] = result[i]


# row = [stock.price['Close'][1], stock.price['Close'][1], stock.price['Close'][1], stock.price['Close'][1], stock.price['Close'][1] ]

# row = [ 10000,10000,10000,10000,10000 ]
#
# result = stock.price['Low'].copy()




#
# from matplotlib import pyplot
# result.plot()
# pyplot.show()


# result.index.name = 'Date'
# for i in range(iData, iData + 10):
#     result[i] = predict[0,i - iData]


# result = result.index.name = 'Date'
#


# import mplfinance as mpf
# apdict = mpf.make_addplot(result)
# mpf.plot(stock.price, title=stock.ticker, type='candle', addplot=apdict)
predicted = [435 , 435 , 436 , 435 , 435]

#
# nFutur = 5
# lendData = len(stock.price)
# import pandas as pd
# for i in range(0, nFutur):
#     idx = stock.price.tail(1).index[0] + pd.Timedelta(minutes=1)
#     stock.price.loc[idx] = stock.price['Low'][-1].copy()
#
# additionalData = stock.price['Low'].copy()
#
# # result.index.name = 'Date'
# for i in range(0, nFutur):
#     additionalData[lendData + i] = predicted[i]


from VisulizeData import VisulizeData
visual = VisulizeData(stock.ticker, stock.price)
# visual.plotCandleStick()
# visual.plotCandlePlus(predicted)
visual.plotCandlePredictData(predicted)

# print(len(dataset))

# from BackTesting import BackTesting
# backTesting = BackTesting()
# backTesting.run()


# closing_price = model.evaluate()

# dataset2 = copy(dataset)
# for i in range(model.trainLengt, len(model.dataSet)):
#     # tikerData.price['Close'][i] = closing_price
#     dataset2['Close'][i] = closing_price[i - model.trainLengt]


# predict = model.predict(len(dataset))
# print('predicted value is: ', predict)
#
# visual = VisulizeData(tikerData, dataset)
# visual.plotCandlePlus([]) #,'Close' 'Open'



# backTesting = BackTesting(ticker, startDate, endDate, SMAcross)
# backTesting.run()



