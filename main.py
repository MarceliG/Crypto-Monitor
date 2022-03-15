"""Main app."""
from download_data import DataMonitor

# Web package
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Graph
import plotly.graph_objs as go


app = dash.Dash(__name__)
app.title = "Crypto Monitor"
app.layout = html.Div(
    [
        # title
        html.H1(
            "My really simple app",
            style={"color": "green", "fontSize": 40, "textAlign": "center"},
        ),
        html.H1(
            "Crypto Monitor",
            style={"color": "orange", "fontSize": 30, "textAlign": "center"},
        ),
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
            ]
        ),
        # slider
        html.H6(
            "Period",
            style={"color": "black", "fontSize": 20, "textAlign": "left"},
        ),
        dcc.Slider(
            step=None,
            marks={
                0: "1 day",
                1: "5 days",
                2: "1 month",
                3: "3 months",
                4: "6 months",
                5: "1 year",
                6: "2 years",
                7: "5 years",
                8: "10 years",
                9: "year to date",
                10: "maximum",
                # 0: "1d",
                # 1: "5d",
                # 2: "1m",
                # 3: "3m",
                # 4: "6m",
                # 5: "1y",
                # 6: "2y",
                # 7: "5y",
                # 8: "10y",
                # 9: "ytd",
                # 10: "max",
            },
            value=10,
            # style={"color": "blue"},
            id="sliderPeriod",
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
    Output(component_id="graphCrypto", component_property="figure"),
    # [
    Input(component_id="dropdownCrypto", component_property="value"),
    Input(component_id="sliderPeriod", component_property="value"),
    # ],
)
# The function argument refers to the input
def update_graph(dropdownCrypto, sliderPeriod):
    """Return crypto graph.

    Args:
        dropdownCrypto: Input on dropdown.

    """
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

    print(sliderPeriod)
    print(chosePeriod)
    historicalCryptoFrame = DataMonitor().GetHistoricalData(
        crypto=dropdownCrypto, period=chosePeriod
    )

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=historicalCryptoFrame.index,
                open=historicalCryptoFrame["Open"],
                high=historicalCryptoFrame["High"],
                low=historicalCryptoFrame["Low"],
                close=historicalCryptoFrame["Close"],
            )
        ]
    )

    fig.update_layout(
        # Add titles
        title="Crypto price evolution",
        yaxis_title="Price (US Dollars)",
        xaxis_title="date",
    )

    # X-Axes
    fig.update_xaxes(
        # removing rangeslider
        rangeslider_visible=False,
        # hide weekends and gaps
        rangebreaks=[dict(bounds=["sat", "mon"])],
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1 month", step="month", stepmode="backward"),
                    dict(count=1, label="1 year", step="year", stepmode="backward"),
                    # dict(count=1, label="1 h", step="hour", stepmode="todate"),
                    # dict(count=6, label="6 h", step="hour", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
