import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class PreProcessing:

    def __init__(self, price):
        self.pricData = price
        self.dataFrame = None

    # # setting index as date
    # def indexInput(self):
    #     self.pricData['Date'] = pd.to_datetime(self.pricData.Date, format='%Y-%m-%d')
    #     self.pricData.index = self.pricData['Date']


    # creating dataframe
    def creatDataFrame(self):
        data = self.pricData.sort_index(ascending=True, axis=0)
        self.dataFrame = pd.DataFrame(index=range(0, len(self.pricData)), columns=['Close'])
        for i in range(0, len(data)):
            # self.dataFrame['Date'][i] = data['Date'][i]
            self.dataFrame['Close'][i] = data['Close'][i]


    # setting index
    def setDataFrameIndex(self):
        # self.dataFrame.index = self.dataFrame.Date

        # self.dataFrame.drop('Date', axis=1)#, inplace=False
        # self.dataFrame = self.dataFrame.values
        print('here')


    def creatDataSet(self):
        # self.indexInput()
        self.creatDataFrame()
        # self.setDataFrameIndex()

        return self.dataFrame


