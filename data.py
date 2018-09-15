from nameko.rpc import rpc
from nameko.timer import timer
import oandaapi


class DataCollector:
    name = "data_service"

    @timer(interval=1)
    def get_ohlc(self):
        """
        :return: List of Market Data with Shape (1,4)
        """

        # TODO: get data from oanda api
        data = [13000, 12500, 12200, 12999]
        print("getting OHLC Data from OANDA API:")
        print(data)

        # TODO: save data to MongoDB



    @rpc
    def get_hictorical_ohlc(self, instrument, from_date, to_date):
        """

        :param instrument:
        :param from_date:
        :param to_date:
        :return:
        """
        # TODO: get historical price data from OANDA API

        historical_ohlc = {'prices': [{'asks': [{'liquidity': 50,
                       'price': '12126.9'},
                      {'liquidity': 50,
                       'price': '12127.0'},
                      {'liquidity': 50,
                       'price': '12127.2'},
                      {'liquidity': 50,
                       'price': '12127.4'}],
             'bids': [{'liquidity': 25,
                       'price': '12124.0'},
                      {'liquidity': 25,
                       'price': '12123.9'},
                      {'liquidity': 50,
                       'price': '12123.8'},
                      {'liquidity': 50,
                       'price': '12123.6'},
                      {'liquidity': 50,
                       'price': '12123.4'}],
             'closeoutAsk': '12127.4',
             'closeoutBid': '12123.4',
             'instrument': 'DE30_EUR',
             'quoteHomeConversionFactors': {'negativeUnits': '1.00000000',
                                            'positiveUnits': '1.00000000'},
             'status': 'non-tradeable',
             'time': '2018-09-14T19:59:00.902942963Z',
             'tradeable': False,
             'type': 'PRICE',
             'unitsAvailable': {'default': {'long': '0',
                                            'short': '0'},
                                'openOnly': {'long': '0',
                                             'short': '0'},
                                'reduceFirst': {'long': '0',
                                                'short': '0'},
                                'reduceOnly': {'long': '0',
                                               'short': '0'}}},
            {'asks': [{'liquidity': 10000000,
                       'price': '0.88990'},
                      {'liquidity': 10000000,
                       'price': '0.89003'}],
             'bids': [{'liquidity': 10000000,
                       'price': '0.88890'},
                      {'liquidity': 10000000,
                       'price': '0.88876'}],
             'closeoutAsk': '0.89003',
             'closeoutBid': '0.88876',
             'instrument': 'EUR_GBP',
             'quoteHomeConversionFactors': {'negativeUnits': '1.12498594',
                                            'positiveUnits': '1.12372177'},
             'status': 'non-tradeable',
             'time': '2018-09-14T20:59:57.782716422Z',
             'tradeable': False,
             'type': 'PRICE',
             'unitsAvailable': {'default': {'long': '1504',
                                            'short': '1504'},
                                'openOnly': {'long': '1504',
                                             'short': '1504'},
                                'reduceFirst': {'long': '1504',
                                                'short': '1504'},
                                'reduceOnly': {'long': '0',
                                               'short': '0'}}}],
 'time': '2018-09-15T08:31:43.006065306Z'}

        print(historical_ohlc)

        # TODO: save the historical data

        return historical_ohlc