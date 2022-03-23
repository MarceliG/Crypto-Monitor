"""Main app."""
from download_data import DataMonitor
from Enum_Time import PeriodEnum, IntervalEnum

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
                    marks={k: value.full_name for k, value in enumerate(PeriodEnum)},
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
                    marks={k: value.full_name for k, value in enumerate(IntervalEnum)},
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
                x=actualPrice.btc_current_Frame["time"],
                y=actualPrice.btc_current_Frame["value"],
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

    short_period = {k: value.short_name for k, value in enumerate(PeriodEnum)}
    chose_period = short_period[sliderPeriod]
    short_interval = {k: value.short_name for k, value in enumerate(IntervalEnum)}
    chose_interval = short_interval[sliderInterval]

    historicalCryptoFrame = DataMonitor().GetHistoricalData(
        crypto=dropdownCrypto, period=chose_period, interval=chose_interval
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
