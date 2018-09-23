from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from keras import optimizers
from keras.utils import to_categorical
import numpy as np
from sklearn.model_selection import train_test_split
import datetime


class Trainer:
    """
    Trainer service. Consumes the data Dat Service.
    Uses the historical OHLC data as input into Neural Network Layer (Keras)
    """
    name = "trainer_service"

    y = RpcProxy("data_service")

    @staticmethod
    def get_model():
        """
        Here we define our model Layers using Keras
        :return: Keras Model Object
        """

        model = Sequential()

        model.add(Dense(units=16,
                        activation='relu',
                        input_shape=(4,)))
        model.add(Dense(units=16,
                        activation='softmax',
                        kernel_regularizer=regularizers.l2(0.001),
                        activity_regularizer=regularizers.l1(0.001)))
        model.add(Dense(units=3,
                        activation='softmax'))

        sgd = optimizers.SGD(lr=0.0001)

        model.compile(loss='categorical_crossentropy',
                      optimizer=sgd,
                      metrics=['accuracy'])
        return model

    week = 60 * 60 * 24 * 7
    decimal_figures = 6
    y_change_threshold = 0.001

    @timer(interval=6000)
    def retrain(self):
        """
        Retrains a model for a specific a) trading instrument, b) timeframe, c) input shape
        """

        # get historical data from data service
        candles = self.y.get_hictorical_ohlc()['candles']
        X, Y = self.process(candles, type='train')

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

        model = self.get_model()
        fit = model.fit(X_train, Y_train, epochs=1000, verbose=True)
        score = model.evaluate(X_test, Y_test, batch_size=128)
        print(score)
        print(model.summary())

        # TODO: Save trained model to disk
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        model.save(filename + '-EUR_USD_H1')

    @rpc
    def process(self, candles, type='train'):
        """
        processing candles to a format/shape consumable for the model
        :param candles: dict/list of Open, High, Low, Close prices
        :return: X: numpy.ndarray, Y: numpy.ndarray
        """

        if type=='train':
            X = np.ndarray(shape=(0, 4))
            Y = np.ndarray(shape=(0, 1))

            # clean and process data
            previous_close = None
            for candle in candles:
                candle = candle['mid']

                candle['o'] = float(candle['o'])
                candle['h'] = float(candle['h'])
                candle['l'] = float(candle['l'])
                candle['c'] = float(candle['c'])

                X = np.append(X,
                              np.array([[
                                  # High 2 Open Price
                                  round(candle['h'] / candle['o'] - 1, self.decimal_figures),
                                  # Low 2 Open Price
                                  round(candle['l'] / candle['o'] - 1, self.decimal_figures),
                                  # Close 2 Open Price
                                  round(candle['c'] / candle['o'] - 1, self.decimal_figures),
                                  # High 2 Low Price
                                  round(candle['h'] / candle['l'] - 1, self.decimal_figures)]]),
                              axis=0)

                # Compute the Y / Target Variable
                if previous_close is not None:
                    y = 0
                    precise_prediction = round(1 - previous_close / candle['c'], self.decimal_figures)

                    # positive price change more growth than threshold
                    if precise_prediction > self.y_change_threshold:
                        y = 1
                    # negative price change with more decline than threshold
                    elif precise_prediction < 0 - self.y_change_threshold:
                        y = 2
                    # price change in between positive and negative threshold
                    elif precise_prediction < self.y_change_threshold and precise_prediction > 0 - self.y_change_threshold:
                        y = 0

                    Y = np.append(Y, np.array([[y]]))
                else:
                    Y = np.append(Y, np.array([[0]]))

                previous_close = candle['c']

            Y = np.delete(Y, 0)
            Y = np.append(Y, np.array([0]))
            Y = to_categorical(Y, num_classes=3)

            return X, Y
        elif type == 'predict':
            print('predict')
            print(candles)
            X = np.ndarray(shape=(0, 4))

            # clean and process data
            candles['o'] = float(candles['o'])
            candles['h'] = float(candles['h'])
            candles['l'] = float(candles['l'])
            candles['c'] = float(candles['c'])

            X = np.append(X,
                          np.array([[
                              # High 2 Open Price
                              round(candles['h'] / candles['o'] - 1, self.decimal_figures),
                              # Low 2 Open Price
                              round(candles['l'] / candles['o'] - 1, self.decimal_figures),
                              # Close 2 Open Price
                              round(candles['c'] / candles['o'] - 1, self.decimal_figures),
                              # High 2 Low Price
                              round(candles['h'] / candles['l'] - 1, self.decimal_figures)]]),
                          axis=0)
            return X