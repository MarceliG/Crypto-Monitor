import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas

import datetime


class Plot:
    def __init__(self):
        pass

    def figure(self, data_BTC):
        # declare figure
        fig = go.Figure()

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=data_BTC.index,
                open=data_BTC["Open"],
                high=data_BTC["High"],
                low=data_BTC["Low"],
                close=data_BTC["Close"],
                name="market data",
            )
        )

        # Add titles
        fig.update_layout(
            title="Bitcoin live share price evolution",
            yaxis_title="Bitcoin Price (US Dollars)",
        )

        # X-Axes
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=15, label="15m", step="minute", stepmode="backward"),
                        dict(count=45, label="45m", step="minute", stepmode="backward"),
                        dict(count=1, label="1h", step="hour", stepmode="todate"),
                        dict(count=6, label="6h", step="hour", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
        )

        # Show
        fig.show()

    def testFigure(self):
        fig = make_subplots(
            rows=3, cols=1, subplot_titles=("Plot 1", "Plot 2", "Plot 3")
        )

        fig.append_trace(
            go.Scatter(
                x=[3, 4, 5],
                y=[1000, 1100, 1200],
            ),
            row=1,
            col=1,
        )

        fig.append_trace(
            go.Scatter(
                x=[2, 3, 4],
                y=[100, 110, 120],
            ),
            row=2,
            col=1,
        )

        fig.append_trace(go.Scatter(x=[0, 1, 2], y=[10, 11, 12]), row=3, col=1)

        # fig.update_layout(height=600, width=600, title_text="Stacked Subplots")
        fig.update_layout(title_text="Stacked Subplots")
        fig.show()

    def simulation(self):
        pass
