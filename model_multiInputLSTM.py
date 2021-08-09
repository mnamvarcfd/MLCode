import copy
import numpy as np
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler


class model_multiInputLSTM:

    def __init__(self, dataFrame, trainPortion):
        self.window = 100
        self.nFutur = 10

        self.trainLengt = int(len(dataFrame) * trainPortion)
        self.testLengt = int(len(dataFrame) - self.trainLengt)

        # creating train and test sets
        dataFrame = dataFrame.values

        # converting dataset into x_train and y_train
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.dataSet = self.scaler.fit_transform(dataFrame)


        self.trainInputData = None
        self.trainOutputData = None
        self.testInputData = None
        self.testOutputData = None
        self.modelLow = None
        self.modelHigh = None
        self.testResult = None

        self.creatTrainData(3)
        self.modelLow = self.creat()
        self.lowScaler = MinMaxScaler(feature_range=(0, 1))
        self.lowScaler.fit_transform(dataFrame[:,3].reshape(-1, 1))

        self.creatTestData()

    # creating train
    def creatTrainData(self, itemPredict):

        trainInput = []
        trainOutput = []
        for i in range(0, self.trainLengt - self.window):
            trainInput.append(self.dataSet[i:i + self.window, :])
            trainOutput.append(self.dataSet[i + self.window : i + self.window + self.nFutur, itemPredict])

        trainInputData = np.array(trainInput)
        trainOutputData = np.array(trainOutput)

        self.trainInputData = np.reshape(trainInputData, (trainInputData.shape[0], trainInputData.shape[1], trainInputData.shape[2]))
        self.trainOutputData = np.reshape(trainOutputData, (trainOutputData.shape[0], trainOutputData.shape[1]))



    # creating test sets
    def creatTestData(self):
        data = self.dataSet

        testInput = []
        testOutput = []
        for i in range(0, self.testLengt):
            testInput.append(data[self.trainLengt - self.window + i:self.trainLengt + i, 0])
            testOutput.append(data[self.trainLengt + i, 0])

        testInput = np.array(testInput)
        self.testInputData = np.reshape(testInput, (testInput.shape[0], testInput.shape[1], 1))

        self.testOutputData = np.array(testOutput)


    # create and fit the LSTM network
    def creat(self):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(self.trainInputData.shape[1], self.trainInputData.shape[2])))
        model.add(LSTM(units=50))
        model.add(Dense(self.nFutur))

        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(self.trainInputData, self.trainOutputData, epochs=1, batch_size=1, verbose=1)

        return model


    def predictNextCand(self, lastData):
        #
        # data = []
        # data.append(self.dataSet[lastData - self.window:lastData, :])
        #
        # data = np.array(data)
        # data = np.reshape(data, (1, data.shape[1], data.shape[2]))
        #
        # low = self.modelHigh.predict(data)
        # low = [low, low, low, low, low]
        # low = np.reshape(low, (1, 5))
        #
        # predictedHigh = self.scaler.inverse_transform(low)
        # print("predicted High value: ", predictedHigh[0][2])

        data = []
        data.append(self.dataSet[lastData - self.window:lastData, :])

        data = np.array(data)
        data = np.reshape(data, (1, data.shape[1], data.shape[2]))

        low = self.modelLow.predict(data)


        predictedLow = self.lowScaler.inverse_transform(low)

        return predictedLow



    #
    # def predictTrend(self, lastData, numCandles):
    #
    #     results = []
    #     data = []
    #     data.append(self.dataSet[lastData - self.length:lastData, :])
    #
    #     data = np.array(data)
    #     data = np.reshape(data, (data.shape[1], data.shape[2], 1))
    #
    #     for i in range(0, numCandles):
    #         data = np.reshape(data, (data.shape[0], data.shape[1], 1))
    #         predicted = self.model.predict(data)
    #
    #         data.reshape(self.length)
    #         data = np.append(data, predicted)
    #         data = np.delete(data, 0)
    #         data = np.reshape(data, (1, data.shape[0], 1))
    #
    #         results = np.append(results, predicted)
    #         results = np.reshape(results, (results.shape[0], 1))
    #
    #     results = self.scaler.inverse_transform(results)
    #
    #     return results



