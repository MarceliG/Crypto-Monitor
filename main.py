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
        html.H1(
            "My really simple app",
            style={"color": "green", "fontSize": 40, "textAlign": "center"},
        ),
        html.H1(
            "Crypto Monitor",
            style={"color": "orange", "fontSize": 30, "textAlign": "center"},
        ),
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
    [Input(component_id="dropdownCrypto", component_property="value")],
)
# The function argument refers to the input
def update_graph(dropdownCrypto):
    """Return crypto graph.

    Args:
        dropdownCrypto: Input on dropdown.

    """
    historicalCryptoFrame = DataMonitor().GetHistoricalData(
        crypto=dropdownCrypto, period="max"
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
