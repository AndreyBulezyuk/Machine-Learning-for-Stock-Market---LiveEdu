from nameko.rpc import rpc, RpcProxy
from nameko.timer import timer
# import oandaapi
from keras.models import load_model
import numpy as np
from pymongo import MongoClient

pyclient = MongoClient()
db = pyclient['liveedu']


class Trader:
    """
    Trader/Predictor service. Consumes the data from MongoDB every x Seconds.
    Uses the data as input into Machine Learning Model via Keras
    Uses the predicted data to either visualize or place order via Oanda API
    """
    name = "trader_service"
    y = RpcProxy("trainer_service")

    @timer(interval=10)
    def predict(self):
        """
        :return: Read Data from MongoDB. Apply ML Model on Data
        """

        # read data from MongoDB
        collection = db['streaming_data']
        newest_candle = collection.find({}) \
            .sort([('candles.0.time', -1)]) \
            .limit(1)

        for nc in newest_candle:
            newest_candle = nc['candles'][0]['mid']

        # get processed X
        X = np.ndarray(shape=(0, 4))

        # clean and process data
        newest_candle['o'] = float(newest_candle['o'])
        newest_candle['h'] = float(newest_candle['h'])
        newest_candle['l'] = float(newest_candle['l'])
        newest_candle['c'] = float(newest_candle['c'])
        decimal_figures = 6
        X = np.append(X,
                      np.array([[
                          # High 2 Open Price
                          round(newest_candle['h'] / newest_candle['o'] - 1, decimal_figures),
                          # Low 2 Open Price
                          round(newest_candle['l'] / newest_candle['o'] - 1, decimal_figures),
                          # Close 2 Open Price
                          round(newest_candle['c'] / newest_candle['o'] - 1, decimal_figures),
                          # High 2 Low Price
                          round(newest_candle['h'] / newest_candle['l'] - 1, decimal_figures)]]),
                      axis=0)

        print(X)

        model = load_model('2018-09-22-11-10-01-EUR_USD_H1')
        Y = model.predict(X)
        print(Y)

        # TODO: visualize or trade on predicted data
