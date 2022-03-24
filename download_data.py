"""Download crypto data as dataFrame."""

from Coin_Market import CoinMarket

# Data Source
import yfinance as yf

from requests import Session
import json
import time

# Format data
import pandas as pd

# URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"

# PARAMETERS = {"slug": "bitcoin", "convert": "USD"}
# HEDERS = {
#     "Accepts": "application/json",
#     "X-CMC_PRO_API_KEY": "8a6e024e-4ad6-4ed6-a43e-0bf97b6327cf",
# }
coin_market = CoinMarket()


class DataMonitor:
    """The object has crypto data."""

    def __init__(self):
        """Initialize."""
        self.btc_current_Frame = pd.DataFrame({"time": [], "value": []})

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
        all_data = yf.download(
            tickers=crypto,
            period=period,
            interval=interval,
        )

        return all_data

    def add_moving_averages(self, dataFrame, *moving_averages: int):
        """Add to dataFrame new column with moving average."""

        for average in moving_averages:
            self.all_data["MA" + str(average)] = (
                self.all_data["Close"].rolling(window=average).mean()
            )
        # data["MA20"] = data["Close"].rolling(window=20).mean()
        # data["MA5"] = data["Close"].rolling(window=5).mean()

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
