from Data import DataMonitor

# Raw Package
import numpy as np
import pandas as pd
import time

# Data Source
import yfinance as yf

# Data viz
import plotly.graph_objs as go


def main():
    # Get Bitcoin data
    # data = yf.download(tickers='BTC-USD', period='max', interval='1d')    # get all graph
    # data = yf.download(tickers='BTC-USD', period='1d', interval='5m')   # get last day
    data_BTC = DataMonitor().GetData('BTC-USD', '1d', '5m')

    # Draw data using pandas
    data_pandas = pd.DataFrame(data_BTC)
    print(data_pandas)

    # declare figure
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data_BTC.index,
                                 open=data_BTC['Open'],
                                 high=data_BTC['High'],
                                 low=data_BTC['Low'],
                                 close=data_BTC['Close'], name='market data'))

    # Add titles
    fig.update_layout(
        title='Bitcoin live share price evolution',
        yaxis_title='Bitcoin Price (US Dollars)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=6, label="6h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Show
    fig.show()


if __name__ == "__main__":
    main()
