from sklearn.preprocessing import MinMaxScaler


class Scaling():

    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    # scaling data
    def scal(self,dataset):
        dataset = self.scaler.fit_transform(dataset)
        return dataset

    # scaling data
    def scal(self,dataset):
        dataset = self.scaler.fit_transform(dataset)

    # invert scaling data
    def invertScal(self,dataset):
        dataset = self.scaler.inverse_transform(dataset)
        return dataset

    # invert scaling data
    def invertScal(self,dataset):
        dataset = self.scaler.inverse_transform(dataset)
