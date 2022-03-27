"""Download crypto data as dataFrame."""

from Coin_Market import CoinMarket

# Data Source
import yfinance as yf

from requests import Session
import json
import time

from ta.trend import MACD
from ta.momentum import StochasticOscillator

# Format data
import pandas as pd

coin_market = CoinMarket()


class DataMonitor:
    """The object has crypto data."""

    def __init__(self):
        """Initialize."""
        self.btc_current_Frame = pd.DataFrame({"time": [], "value": []})
        self.all_data: pd.core.frame.DataFrame

    def get_historical_data(self, crypto="BTC-USD", period="max", interval="1d"):
        """Get Historical crypto data.

        Args:
            crypto: name of cash.
            period: when to start downloading data. 1d, 5d, 1mo, 3mo, 6mo,
            1y, 2y, 5y, 10y, ytd, max
            intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo.

        Returns:
            cryptoFrame: dataFrame.

        """
        self.all_data = yf.download(
            tickers=crypto,
            period=period,
            interval=interval,
        )

        # TODO use method bellow.
        self.all_data["MA20"] = self.all_data["Close"].rolling(window=20).mean()
        self.all_data["MA5"] = self.all_data["Close"].rolling(window=5).mean()

        return self.all_data

    def add_moving_averages(self, dataFrame, *moving_averages: int):
        """Add to dataFrame new column with moving average."""

        for average in moving_averages:
            self.all_data["MA" + str(average)] = (
                self.all_data["Close"].rolling(window=average).mean()
            )

    def get_MACD(self, dataFrame):
        """Create frame as Moving Average Convergence / Divergence (MACD).

        Args:
            dataFrame : frame

        Returns:
            return MACD.
        """
        macd = MACD(
            close=dataFrame["Close"],
            window_slow=26,
            window_fast=12,
            window_sign=9,
        )
        return macd

    def get_stochastic(self, dataFrame):
        """Crate frame as stochastic.

        Args:
            dataFrame: frame

        Returns:
            Stochastic.
        """
        stoch = StochasticOscillator(
            high=dataFrame["High"],
            close=dataFrame["Close"],
            low=dataFrame["Low"],
            window=14,
            smooth_window=3,
        )

        return stoch

    def get_current_data(self):
        """Return frame with 2 columns, date and value.

        Returns:
            frame: frame with date and BTC-USD
        """

        new_row = pd.Series(
            data={
                "time": self.get_actual_time(),
                "value": self.get_actual_price(),
            }
        )
        self.btc_current_Frame = self.btc_current_Frame.append(
            new_row,
            ignore_index=True,
        )
        return self.btc_current_Frame

    def get_actual_price(self):
        """Return actual price.

        Returns:
            price
        """

        session = Session()
        session.headers.update(coin_market.HEDERS)

        response = session.get(coin_market.URL, params=coin_market.PARAMETERS)
        # pprint.pprint(json.loads(response.text)['data'])
        return json.loads(response.text)["data"]["1"]["quote"]["USD"]["price"]

    def get_actual_time(self):
        """Return actual time.

        Returns:
            time
        """

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        return current_time
