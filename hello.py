from nameko.timer import timer

class Data:
    name = "data_service"

    @timer(interval=60*5)
    def get_ohlc(self):

        oanda_data = []

        # TODO: Get Data from OANDA API


        # TODO: Save Dat from Oanda API to Mongo DB


        return oanda_data
