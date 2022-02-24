
# Data Source
import yfinance as yf

import pandas as pd


class DataMonitor():
    def __init__(self):
        self.data_all: pd.core.frame.DataFrame
        self.data_last_day: pd.core.frame.DataFrame

    def GetData(self, currency, period, interval):
        # Get Bitcoin data
        self.data_all = yf.download(
            tickers='BTC-USD', period='max', interval='1d')    # get all graph

        self.data = yf.download(
            tickers=currency, period=period, interval=interval)   # get last day

        frame = [self.data_all, self.data]
        result = pd.concat(frame)

        return result
