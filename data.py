from nameko.rpc import rpc
from nameko.timer import timer
import oandaapi

class DataCollector:
    name = "data_service"

    @timer(interval=60*5)
    def get_ohlc(self):
        """
        :return: List of Market Data with Shape (1,4)
        """

        # TODO: get data from oanda api
        data = [13000, 12500, 12200, 12999]
        print("getting OHLC Data from OANDA API:")
        print(data)

        # TODO: save data to MongoDB


    # TODO:
    @rcp
    def get_hictorical_ohlc(self):
        return historical_ohlc