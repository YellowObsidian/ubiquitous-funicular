import plotly.graph_objects as go

def get_candlestick_fig(price_df):
    return go.Figure(data=[go.Candlestick(x=list(reversed(price_df['start_time'])),
                open=list(reversed(price_df['open_price'])),
                high=list(reversed(price_df['high_price'])),
                low=list(reversed(price_df['low_price'])),
                close=list(reversed(price_df['close_price'])))])