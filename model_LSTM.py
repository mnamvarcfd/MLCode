import copy
import numpy as np
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler



class model_LSTM:

    def __init__(self, dataFrame, trainPortion):
        self.length = 60
        self.trainLengt = int(len(dataFrame) * trainPortion)
        self.testLengt = int(len(dataFrame) - self.trainLengt)

        # creating train and test sets
        dataFrame = dataFrame.values

        # converting dataset into x_train and y_train
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        dataFrame = self.scaler.fit_transform(dataFrame)

        self.dataSet = dataFrame

        self.trainInputData = None
        self.trainOutputData = None
        self.testInputData = None
        self.testOutputData = None
        self.model = None
        self.testResult = None

        self.creatTrainData()
        self.creat()

        self.creatTestData()

    # creating train
    def creatTrainData(self):
        data = self.dataSet[0:self.trainLengt, :]

        trainInput = []
        trainOutput = []
        for i in range(self.length, len(data)):
            trainInput.append(data[i - self.length:i, 0])
            trainOutput.append(data[i, 0])

        trainInputData = np.array(trainInput)

        self.trainInputData = np.reshape(trainInputData, (trainInputData.shape[0], trainInputData.shape[1], 1))
        self.trainOutputData = np.array(trainOutput)


    # creating test sets
    def creatTestData(self):
        data = self.dataSet

        testInput = []
        testOutput = []
        for i in range(0, self.testLengt):
            testInput.append(data[self.trainLengt-self.length+i:self.trainLengt+i, 0])
            testOutput.append(data[self.trainLengt + i, 0])

        testInput = np.array(testInput)
        self.testInputData = np.reshape(testInput, (testInput.shape[0], testInput.shape[1], 1))

        self.testOutputData = np.array(testOutput)


    # create and fit the LSTM network
    def creat(self):
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(self.trainInputData.shape[1], 1)))
        self.model.add(LSTM(units=50))
        self.model.add(Dense(1))

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(self.trainInputData, self.trainOutputData, epochs=1, batch_size=1, verbose=2)


    def predictNextCand(self, lastData):

        data = []
        data.append(self.dataSet[lastData - self.length:lastData, :])

        data = np.array(data)

        data = np.reshape(data, (data.shape[0], data.shape[1], 1))
        predicted = self.model.predict(data)
        predicted = self.scaler.inverse_transform(predicted)  # scaling data
        # print("predicted value: ", predicted)
        return predicted


    def predictTrend(self, lastData, numCandles):

        results = []
        data = []
        data.append(self.dataSet[lastData - self.length:lastData, :])

        data = np.array(data)

        for i in range(0, numCandles):
            data = np.reshape(data, (data.shape[0], data.shape[1], 1))
            predicted = self.model.predict(data)

            data.reshape(self.length)
            data = np.append(data, predicted)
            data = np.delete(data, 0)
            data = np.reshape(data, (1, data.shape[0], 1))

            results = np.append(results, predicted)
            results = np.reshape(results, (results.shape[0], 1))

        results = self.scaler.inverse_transform(results)

        return results



    def evaluate(self):
        testResult = self.model.predict(self.testInputData)
        testResult = self.scaler.inverse_transform(testResult)  # scaling data

        return testResult