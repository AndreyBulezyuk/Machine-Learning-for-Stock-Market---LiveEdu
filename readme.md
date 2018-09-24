#install
pip3 install -r requirements.txt

1. Adjust CronJob Intervals in trainer, trader and data services
2. Create a oandaapi.py file with a variable with you API-Key from oanda.com Broker

#run services
nameko run data
nameko run trainer
nameko run trader

Trader Service only prints out the prediction. You can chose what you do with the prediction (e.g. place order, visualize, etc.)

Recommended Extensions:
- Change Keras Input Shape to a LSTM Layer
- Let Trader Service chose the most recent saved model-weights.