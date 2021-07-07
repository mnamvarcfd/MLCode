# import packages
from datetime import date  # date and time functionality

import numpy as np
from matplotlib import pyplot as plt
# from SMAcross import SMAcross

# ======================input======================
from mpmath import mpf

today = date.today()
print("Today's date:", today)
endDate = date(2021, 7, 2)
startDate = date(2021, 6, 28)
interval = "1m"
ticker = 'MSFT'
# ======================get price data======================
# print('============', endDate-startDate)


from GetData import GetData
MSF = GetData(ticker, startDate, endDate, interval)
# MSF.plotCandleStick()
# MSF.writePric()


from PreProcessing import PreProcessing
preProcessing = PreProcessing(MSF.price)
dataFrame = preProcessing.creatDataFrame()

# dataFrame['Close'].plot()
# plt.show()


from model_LSTM import model_LSTM
# model = model_LSTM(dataFrame, 0.7)
# model.predictNextCand(len(dataFrame)-5)
# result = model.predictTrend(len(dataFrame)-500, 500)
# result = np.array(result)
# plt.plot(result)
# plt.show()





# print(len(dataset))

from BackTesting import BackTesting
backTesting = BackTesting(ticker, startDate, endDate, interval)
backTesting.run()


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



