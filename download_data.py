
# Data Source
import yfinance as yf

from requests import Request, Session
import json
import pprint
import time

# Format data
import pandas as pd

URL = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'


class DataMonitor():
    def __init__(self):
        self.data_all: pd.core.frame.DataFrame = yf.download(
            tickers='BTC-USD', period='max', interval='1d')    # get all graph
        self.data_last_day: pd.core.frame.DataFrame

        self.btc_current = {}

        # ########
        self.parameters = {
            "slug": "bitcoin",
            "convert": "PLN"}
        self.heders = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": "8a6e024e-4ad6-4ed6-a43e-0bf97b6327cf"
        }
        # self.btcFrame = pd.DataFrame([],columns=['time', 'value'])
        self.btcFrame = pd.DataFrame({'time': [], 'value': []})

    def GetHistoricalData(self, crypto='BTC-USD', period="1d", interval='5m'):
        # Get Historical crypto data
        self.data = yf.download(
            tickers=crypto, period=period, interval=interval)   # get last day
        return self.data

    def GetCurrentData(self):
        newData = pd.DataFrame({'time': [self.GetActualTime()], 'value': [self.GetActualPrice()]})
        self.btcFrame = self.btcFrame.append(newData, ignore_index=True)
        return self.btcFrame

    def GetActualPrice(self):

        session = Session()
        session.headers.update(self.heders)

        response = session.get(URL, params=self.parameters)
        # pprint.pprint(json.loads(response.text)['data'])
        return json.loads(response.text)[
            'data']['1']['quote']['PLN']['price']

    def GetActualTime(self):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time
