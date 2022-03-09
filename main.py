from download_data import DataMonitor
from draw_plot import Plot

# Raw Package
import numpy as np
import pandas as pd
import time

# Web package
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Data Source
import yfinance as yf

# Graph
import plotly
import plotly.graph_objs as go

from collections import deque
import random


# start app
X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

# App layout
app = dash.Dash(__name__)
app.title = "Crypto Monitor"
btcFrame = DataMonitor().GetCurrentData()
app.layout = html.Div([
    # dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
    # html.Div(id='dd-output-container'),

    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id='graph-update',
                 interval=1000),
])


@app.callback(
    # Output('dd-output-container', 'children'),
    Output('live-graph', 'figure'),
    Input('graph-update', 'interval'),
    # Input('demo-dropdown', 'value')
)
# def update_output(value):
# if many outputs, add then to return
# return f'You have selected {value}'
def update_graph_scatter(n):
    # X = X.append(btcFrame['time'].iloc[-1])
    # Y = Y.append(btcFrame['value'].iloc[-1])
    # print(btcFrame)
    # print('X:', X, 'Y:', Y)

    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1, 0.1))
    print(X)
    print(Y)

    data = plotly.graph_objs.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode='lines+markers'
    )
    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]), yaxis=dict(range=[min(Y), max(Y)]),)}

# def main():
#     # Get Bitcoin data
#     data_bitcoin = DataMonitor()
#     print(type(data_bitcoin.data_all))
#     data_BTC = data_bitcoin.GetHistoricalData('BTC-USD', '1y', '1d')
#     # print(data_BTC)

#     i = 0
#     while i < 5:
#         btc = data_bitcoin.GetActualPrice()
#         # print(btc)
#         i += 1
#         time.sleep(1)
#         print(data_bitcoin.GetCurrentData())

#     # Plot().figure(data_BTC)
#     # Plot().testFigure()


if __name__ == "__main__":
    # main()
    app.run_server(debug=True)
