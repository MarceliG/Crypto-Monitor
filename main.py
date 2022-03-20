"""Main app."""
from download_data import DataMonitor

# Web package
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Graph
import plotly.graph_objs as go

actualPrice = DataMonitor()

app = dash.Dash(__name__)
app.title = "Crypto Monitor"
app.layout = html.Div(
    [
        # title
        html.H1(
            "Crypto Monitor",
            style={
                "color": "green",
                "fontSize": 40,
                "textAlign": "center",
            },
        ),
        #######
        html.Div(
            [
                html.H6(
                    "Live Bitcoin graph",
                    style={
                        "color": "black",
                        "fontSize": 20,
                        "textAlign": "left",
                    },
                ),
                dcc.Graph(id="graphLive"),
                dcc.Interval(
                    id="intervalComponent",
                    interval=10 * 1000,  # in milliseconds
                    n_intervals=0,
                ),
            ],
        ),
        #######
        # dropdown
        html.Div(
            [
                # Label above dropdown
                html.Label(["Select crypto"]),
                # Dropdown
                dcc.Dropdown(
                    id="dropdownCrypto",
                    options=[
                        {"label": "Bitcoin - BTC", "value": "BTC-USD"},
                        {"label": "Etherium - ETH", "value": "ETH-USD"},
                        {"label": "Litecoin - LTC", "value": "LTC-USD"},
                        {"label": "Stellar - XLM", "value": "XLM-USD"},
                    ],
                    value="BTC-USD",
                    multi=False,
                    clearable=False,
                    style={"width": "50%"},
                ),
            ],
        ),
        # slider period
        html.Div(
            [
                html.H6(
                    "Period",
                    style={
                        "color": "black",
                        "fontSize": 20,
                        "textAlign": "left",
                    },
                ),
                dcc.Slider(
                    step=None,
                    marks={
                        0: "1 day",
                        1: "5 days",
                        2: "1 month",
                        3: "3 months",
                        4: "6 months",
                        5: "year to date",
                        6: "1 year",
                        7: "2 years",
                        8: "5 years",
                        9: "10 years",
                        10: "maximum",
                    },
                    value=5,
                    id="sliderPeriod",
                ),
                # slider interval
                html.H6(
                    "Interval",
                    style={
                        "color": "black",
                        "fontSize": 20,
                        "textAlign": "left",
                    },
                ),
                dcc.Slider(
                    step=None,
                    marks={
                        0: "1 minute",
                        1: "2 minute",
                        2: "5 minute",
                        3: "15 minute",
                        4: "30 minute",
                        5: "60 minute",
                        6: "90 minute",
                        7: "1 hour",
                        8: "1 day",
                        9: "5 day",
                        10: "1 week",
                        11: "1 month",
                        12: "3 month",
                    },
                    value=8,
                    id="sliderInterval",
                ),
            ]
        ),
        # Graph
        html.Div(
            [
                dcc.Graph(id="graphCrypto"),
            ]
        ),
    ]
)


# ----------------------------------------
@app.callback(
    [
        Output(
            component_id="graphLive",
            component_property="figure",
        ),
        Output(
            component_id="graphCrypto",
            component_property="figure",
        ),
    ],
    [
        Input(
            component_id="intervalComponent",
            component_property="n_intervals",
        ),
        Input(
            component_id="dropdownCrypto",
            component_property="value",
        ),
        Input(
            component_id="sliderPeriod",
            component_property="value",
        ),
        Input(
            component_id="sliderInterval",
            component_property="value",
        ),
    ],
)
# The function argument refers to the input
def update_graph(
    intervalComponent,
    dropdownCrypto,
    sliderPeriod,
    sliderInterval,
):
    """Return crypto graph.

    Args:
        intervalComponent: The time that determines how quickly the page
        will refresh.
        dropdownCrypto: Input on dropdown.
        sliderPeriod: Chosen period historical graph.
        sliderInterval: Chosen interval historical graph.
    """

    actualPrice.GetCurrentData()

    figureCryptoLive = go.Figure(
        data=[
            go.Scatter(
                x=actualPrice.btcFrame["time"],
                y=actualPrice.btcFrame["value"],
                mode="lines+markers",
                line=dict(
                    color="green",
                    width=2,
                ),
            ),
        ]
    )

    figureCryptoLive.update_layout(
        # Add titles
        title="BTC live updates every 10s",
        yaxis_title="Price (US Dollars)",
        xaxis_title="time",
        autosize=True,
    )
    ####################

    # TODO ENUM
    if sliderPeriod == 0:
        chosePeriod = "1d"
    elif sliderPeriod == 1:
        chosePeriod = "5d"
    elif sliderPeriod == 2:
        chosePeriod = "1m"
    elif sliderPeriod == 3:
        chosePeriod = "3m"
    elif sliderPeriod == 4:
        chosePeriod = "6m"
    elif sliderPeriod == 5:
        chosePeriod = "1y"
    elif sliderPeriod == 6:
        chosePeriod = "2y"
    elif sliderPeriod == 7:
        chosePeriod = "5y"
    elif sliderPeriod == 8:
        chosePeriod = "10y"
    elif sliderPeriod == 9:
        chosePeriod = "ytd"
    elif sliderPeriod == 10:
        chosePeriod = "max"

    if sliderInterval == 0:
        choseInterval = "1m"
    elif sliderInterval == 1:
        choseInterval = "2m"
    elif sliderInterval == 2:
        choseInterval = "5m"
    elif sliderInterval == 3:
        choseInterval = "15m"
    elif sliderInterval == 4:
        choseInterval = "30m"
    elif sliderInterval == 5:
        choseInterval = "60m"
    elif sliderInterval == 6:
        choseInterval = "90m"
    elif sliderInterval == 7:
        choseInterval = "1h"
    elif sliderInterval == 8:
        choseInterval = "1d"
    elif sliderInterval == 9:
        choseInterval = "5d"
    elif sliderInterval == 10:
        choseInterval = "1wk"
    elif sliderInterval == 11:
        choseInterval = "1mo"
    elif sliderInterval == 12:
        choseInterval = "3mo"

    historicalCryptoFrame = DataMonitor().GetHistoricalData(
        crypto=dropdownCrypto, period=chosePeriod, interval=choseInterval
    )

    figureCryptoEvolution = go.Figure(
        data=[
            go.Candlestick(
                x=historicalCryptoFrame.index,
                open=historicalCryptoFrame["Open"],
                high=historicalCryptoFrame["High"],
                low=historicalCryptoFrame["Low"],
                close=historicalCryptoFrame["Close"],
            ),
        ]
    )

    figureCryptoEvolution.update_layout(
        # Add titles
        title="Crypto price evolution",
        yaxis_title="Price (US Dollars)",
        xaxis_title="date",
    )

    # X-Axes
    figureCryptoEvolution.update_xaxes(
        # removing rangeslider
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list(
                [
                    dict(
                        count=1,
                        label="1 month",
                        step="month",
                        stepmode="backward",
                    ),
                    dict(
                        count=1,
                        label="1 year",
                        step="year",
                        stepmode="backward",
                    ),
                    dict(step="all"),
                ]
            )
        ),
    )
    return figureCryptoLive, figureCryptoEvolution


if __name__ == "__main__":
    app.run_server(debug=True)
