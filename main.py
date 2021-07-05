# import packages
from datetime import date  # date and time functionality

# from SMAcross import SMAcross

# ======================input======================
today = date.today()
print("Today's date:", today)
endDate = date(2021, 7, 2)
startDate = date(2021, 6, 28)
interval = "1m"
ticker = 'MSFT'
# ======================get price data======================

from GetData import GetData
MSF = GetData(ticker, startDate, endDate, interval)
# import yfinance as yf
# price = yf.download(ticker, period="2d", interval="1m", auto_adjust=True)
MSF.plotCandleStick()
MSF.writePric()



# preProcessing = PreProcessing(tikerData)
# dataset = preProcessing.creatDataSet()

# dataset['Close'].plot()
# plt.show()

# model = model_LSTM(dataset, 0.7)

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


