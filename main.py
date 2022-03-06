from download_data import DataMonitor
from draw_plot import Plot

# Raw Package
import numpy as np
import pandas as pd
import time


# Data Source
import yfinance as yf


def main():
    # Get Bitcoin data
    data_bitcoin = DataMonitor()
    print(type(data_bitcoin.data_all))
    data_BTC = data_bitcoin.GetHistoricalData('BTC-USD', '1y', '1d')
    # print(data_BTC)

    i = 0
    while i < 5:
        btc = data_bitcoin.GetActualPrice()
        # print(btc)
        i += 1
        time.sleep(1)
        print(data_bitcoin.GetCurrentData())

    # Plot().figure(data_BTC)
    # Plot().testFigure()


if __name__ == "__main__":
    main()
