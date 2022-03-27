"""Main app."""
from download_data import DataMonitor
from Enum_Time import PeriodEnum, IntervalEnum

# Web package
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Graph
import plotly.graph_objs as go

actual_price = DataMonitor()

app = dash.Dash(__name__)
app.title = "Crypto Monitor"
app.layout = html.Div(
    [
        # title
        html.Div(
            [
                html.H1(
                    "Crypto Monitor",
                    style={
                        "color": "green",
                        "fontSize": 40,
                        "textAlign": "center",
                    },
                ),
                html.P(
                    "My first Dash app",
                    style={
                        "textAlign": "center",
                    },
                ),
            ],
            style={"padding": "30px", "backgroundColor": "#ebac3d"},
        ),
        #######
        html.Div(
            [
                dcc.Graph(id="graph_live"),
                dcc.Interval(
                    id="interval_component",
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
                    id="dropdown_crypto",
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
                    id="slider_period",
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
                    id="slider_interval",
                ),
            ]
        ),
        # Graph
        html.Div(
            [
                dcc.Graph(id="graph_crypto"),
            ]
        ),
    ]
)


# ----------------------------------------
@app.callback(
    [
        Output(
            component_id="graph_live",
            component_property="figure",
        ),
        Output(
            component_id="graph_crypto",
            component_property="figure",
        ),
    ],
    [
        Input(
            component_id="interval_component",
            component_property="n_intervals",
        ),
        Input(
            component_id="dropdown_crypto",
            component_property="value",
        ),
        Input(
            component_id="slider_period",
            component_property="value",
        ),
        Input(
            component_id="slider_interval",
            component_property="value",
        ),
    ],
)
# The function argument refers to the input
def update_graph(
    interval_component,
    dropdown_crypto,
    slider_period,
    slider_interval,
):
    """Return crypto graph.

    Args:
        interval_component: The time that determines how quickly the page
        will refresh.
        dropdown_crypto: Input on dropdown.
        slider_period: Chosen period historical graph.
        slider_interval: Chosen interval historical graph.
    """

    actual_price.get_current_data()

    figure_crypto_live = go.Figure(
        data=[
            go.Scatter(
                x=actual_price.btc_current_Frame["time"],
                y=actual_price.btc_current_Frame["value"],
                mode="lines+markers",
                line=dict(
                    color="green",
                    width=2,
                ),
            ),
        ]
    )

    figure_crypto_live.update_layout(
        # Add titles
        title="Live Bitcoin(BTC) graph updates every 10s",
        yaxis_title="Price (US Dollars)",
        xaxis_title="time",
        autosize=True,
    )
    ####################

    short_period = {k: value.short_name for k, value in enumerate(PeriodEnum)}
    chose_period = short_period[slider_period]
    short_interval = {k: value.short_name for k, value in enumerate(IntervalEnum)}
    chose_interval = short_interval[slider_interval]

    historical_crypto_frame = DataMonitor().get_historical_data(
        crypto=dropdown_crypto, period=chose_period, interval=chose_interval
    )

    figure_crypto_evolution = go.Figure(
        data=[
            go.Candlestick(
                x=historical_crypto_frame.index,
                open=historical_crypto_frame["Open"],
                high=historical_crypto_frame["High"],
                low=historical_crypto_frame["Low"],
                close=historical_crypto_frame["Close"],
            ),
        ]
    )

    figure_crypto_evolution.update_layout(
        # Add titles
        title="Crypto price evolution",
        yaxis_title="Price (US Dollars)",
        xaxis_title="date",
    )

    # X-Axes
    figure_crypto_evolution.update_xaxes(
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
    return figure_crypto_live, figure_crypto_evolution


if __name__ == "__main__":
    app.run_server(debug=True)
