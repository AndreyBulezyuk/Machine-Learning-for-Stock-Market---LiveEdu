from nameko.rpc import rpc
from nameko.timer import timer
import oandaapi
import json
from oandapyV20 import API    # the client
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.instruments as instruments
from pymongo import MongoClient
pyclient = MongoClient()
db = pyclient['liveedu']

access_token = oandaapi.oandaAPI
accountID = "001-004-1129934-001"
client = API(access_token=access_token, environment="live")

GRANULARITY = "H1"
INSTRUMENT = "EUR_USD"

class DataCollector:
    name = "data_service"

    @timer(interval=10)
    def get_ohlc(self):
        """
        :return: List of Market Data with Shape (1,4)
        """

        # get data from oanda api
        params = {
            "granularity": GRANULARITY,
            "count": 2
        }
        newest_candle = instruments.InstrumentsCandles(INSTRUMENT,  params)
        newest_candle = client.request(newest_candle)

        collection = db['streaming_data']

        current_timestamp = newest_candle['candles'][0]['time']
        find_double = collection.find_one({'candles.0.time': current_timestamp})

        # check if candle, with current timestamp is not present.
        if find_double is not None:
            return False

        # save data to MongoDB
        collection.insert_one(newest_candle)


    @rpc
    def get_hictorical_ohlc(self, instrument=INSTRUMENT, granularity=GRANULARITY, count=5000):
        """

        :param instrument:
        :param from_date:
        :param to_date:
        :return:
        """

        # get historical price data from OANDA API
        params = {
            "granularity": granularity,
            "count": count
        }
        hist_data = instruments.InstrumentsCandles(instrument,  params)
        hist_data = client.request(hist_data)

        # save the historical data
        collection = db['historical_ohlc']
        collection.insert_one(hist_data)

        del hist_data['_id']
        print(hist_data)
        print(type(hist_data))


        return hist_data