import pandas as pd



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

        return self.dataFrame