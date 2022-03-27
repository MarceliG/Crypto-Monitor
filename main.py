"""Main app."""
from download_data import DataMonitor
from Enum_Time import PeriodEnum, IntervalEnum

# Web package
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Graph
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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
    macd = DataMonitor().get_MACD(historical_crypto_frame)
    stochastic = DataMonitor().get_stochastic(historical_crypto_frame)

    figure_crypto_evolution = make_subplots(
        rows=4,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.01,
        row_heights=[0.5, 0.1, 0.2, 0.2],
    )

    figure_crypto_evolution.append_trace(
        go.Candlestick(
            x=historical_crypto_frame.index,
            open=historical_crypto_frame["Open"],
            high=historical_crypto_frame["High"],
            low=historical_crypto_frame["Low"],
            close=historical_crypto_frame["Close"],
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    figure_crypto_evolution.add_trace(
        go.Scatter(
            x=historical_crypto_frame.index,
            y=historical_crypto_frame["MA20"],
            opacity=0.5,
            line=dict(color="blue", width=2),
            name="Moving Average 20",
        ),
        row=1,
        col=1,
    )
    figure_crypto_evolution.add_trace(
        go.Scatter(
            x=historical_crypto_frame.index,
            y=historical_crypto_frame["MA5"],
            opacity=0.5,
            line=dict(color="orange", width=2),
            name="Moving Average 5",
        ),
        row=1,
        col=1,
    )

    colorsVolume = [
        "green" if row["Open"] - row["Close"] >= 0 else "red"
        for index, row in historical_crypto_frame.iterrows()
    ]
    figure_crypto_evolution.add_trace(
        go.Bar(
            x=historical_crypto_frame.index,
            y=historical_crypto_frame["Volume"],
            marker_color=colorsVolume,
        ),
        row=2,
        col=1,
    )

    colorsMCDA = ["green" if val >= 0 else "red" for val in macd.macd_diff()]
    # Plot MACD trace on 3rd row
    figure_crypto_evolution.add_trace(
        go.Bar(
            x=historical_crypto_frame.index,
            y=macd.macd_diff(),
            marker_color=colorsMCDA,
        ),
        row=3,
        col=1,
    )
    figure_crypto_evolution.add_trace(
        go.Scatter(
            x=historical_crypto_frame.index,
            y=macd.macd(),
            line=dict(color="black", width=2),
        ),
        row=3,
        col=1,
    )
    figure_crypto_evolution.add_trace(
        go.Scatter(
            x=historical_crypto_frame.index,
            y=macd.macd_signal(),
            line=dict(color="blue", width=1),
        ),
        row=3,
        col=1,
    )
    # Plot stochastics trace on 4th row
    figure_crypto_evolution.add_trace(
        go.Scatter(
            x=historical_crypto_frame.index,
            y=stochastic.stoch(),
            line=dict(color="black", width=2),
        ),
        row=4,
        col=1,
    )
    figure_crypto_evolution.add_trace(
        go.Scatter(
            x=historical_crypto_frame.index,
            y=stochastic.stoch_signal(),
            line=dict(color="blue", width=1),
        ),
        row=4,
        col=1,
    )
    # update layout by changing the plot size, hiding legends & rangeslider, and removing gaps between dates
    figure_crypto_evolution.update_layout(
        height=900,
        width=1200,
        showlegend=False,
        xaxis_rangeslider_visible=False,
    )

    # Add titles
    figure_crypto_evolution.update_layout(
        title="Crypto price evolution",
        yaxis_title="Price (US Dollars)",
    )

    # update y-axis label
    figure_crypto_evolution.update_yaxes(title_text="Price", row=1, col=1)
    figure_crypto_evolution.update_yaxes(title_text="Volume", row=2, col=1)
    figure_crypto_evolution.update_yaxes(
        title_text="MACD", showgrid=False, row=3, col=1
    )
    figure_crypto_evolution.update_yaxes(title_text="Stoch", row=4, col=1)

    # # removing white space
    # figure_crypto_evolution.update_layout(
    #     margin=go.layout.Margin(
    #         l=100,  # left margin
    #         r=100,  # right margin
    #         b=100,  # bottom margin
    #         t=100,  # top margin
    #     )
    # )

    return figure_crypto_live, figure_crypto_evolution


if __name__ == "__main__":
    app.run_server(debug=True)
