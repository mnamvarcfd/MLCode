import copy
import numpy as np
from keras.layers import Dense, LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

class model_LSTM:

    def __init__(self, dataSet, trainPortion):
        self.trainLengt = int(len(dataSet) * trainPortion)
        self.testLengt = int(len(dataSet) - self.trainLengt)

        # creating train and test sets
        dataSet = dataSet.values

        # converting dataset into x_train and y_train
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        dataSet = self.scaler.fit_transform(dataSet)

        self.dataSet = dataSet

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
        for i in range(60, len(data)):
            trainInput.append(data[i - 60:i, 0])
            trainOutput.append(data[i, 0])

        trainInputData = np.array(trainInput)

        self.trainInputData = np.reshape(trainInputData, (trainInputData.shape[0], trainInputData.shape[1], 1))
        self.trainOutputData = np.array(trainOutput)

    #
    # # creating test sets
    # def creatTestData(self):
    #     data = self.dataSet[self.trainLengt - 60:, :]
    #
    #     testInput = []
    #     testOutput = []
    #     for i in range(0, self.testLengt):
    #         testInput.append(data[i:i + 60, 0])
    #         testOutput.append(data[60 + i, 0])
    #
    #     testInput = np.array(testInput)
    #     self.testInputData = np.reshape(testInput, (testInput.shape[0], testInput.shape[1], 1))
    #
    #     self.testOutputData = np.array(testOutput)

    # create and fit the LSTM network


    # creating test sets
    def creatTestData(self):
        data = self.dataSet

        testInput = []
        testOutput = []
        for i in range(0, self.testLengt):
            testInput.append(data[self.trainLengt-60+i:self.trainLengt+i, 0])
            testOutput.append(data[self.trainLengt + i, 0])

        testInput = np.array(testInput)
        self.testInputData = np.reshape(testInput, (testInput.shape[0], testInput.shape[1], 1))

        self.testOutputData = np.array(testOutput)


    def creat(self):
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(self.trainInputData.shape[1], 1)))
        self.model.add(LSTM(units=50))
        self.model.add(Dense(1))

        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(self.trainInputData, self.trainOutputData, epochs=1, batch_size=1, verbose=2)

    def evaluate(self):
        testResult = self.model.predict(self.testInputData)
        testResult = self.scaler.inverse_transform(testResult)  # scaling data

        return testResult




    def predict(self, lastData):

        data = []
        data.append(self.dataSet[lastData - 60:lastData, :])

        data = np.array(data)

        data = np.reshape(data, (data.shape[0], data.shape[1], 1))
        predicted = self.model.predict(data)
        predicted = self.scaler.inverse_transform(predicted)  # scaling data

        return predicted

    #
    # def predict(self, lastData, numCandles):
    #
    #     results = []
    #     data = []
    #     data.append(self.dataSet[lastData - 60:lastData, :])
    #
    #     data = np.array(data)
    #
    #     for i in range(0, numCandles):
    #         data = np.reshape(data, (data.shape[0], data.shape[1], 1))
    #         predicted = self.model.predict(data)
    #
    #         data = np.append(data, predicted)
    #
    #         data = np.delete(data, 0, 0)
    #
    #         results = np.append(results, predicted)
    #
    #     results = self.scaler.inverse_transform(results)
    #     return results