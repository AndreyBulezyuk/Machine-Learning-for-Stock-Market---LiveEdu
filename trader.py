from hello.rpc import rpc
from hello.timer import timer
import oandaapi

class Trader:
    """
    Trader/Predictor service. Consumes the data from MongoDB every x Seconds.
    Uses the data as input into Machine Learning Model via Keras
    Uses the predicted data to either visualize or place order via Oanda API
    """
    name = "trader_service"

    @timer(interval=5*60)
    def predict(self):
        """
        :return: Read Data from MongoDB. Apply ML Model on Data
        """

        # TODO: read data from MongoDB

        data = [13000, 12500, 12200, 12999]
        print("getting OHLC Data from OANDA API:")
        print(data)

        # TODO: visualize or trade on predicted data
        