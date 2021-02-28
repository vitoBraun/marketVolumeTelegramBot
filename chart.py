import plotly.graph_objects as go
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
from plotly.subplots import make_subplots
import requests
from threading import Thread
import plotly.graph_objs as go


class Chart(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.run()

    def run(self):
        timing = 30
        chart_gen()
        while True:
            timing -= 1
            time.sleep(1)
            if timing == 0:
                chart_gen()
                timing = 30
                continue


def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(
        now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


def chart_gen():
    df = pd.read_csv('stockdata.csv', names=[
        "date", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "Number_of_trades", "tn", "tnfg", "Ignore"])
    date = []
    for i in df['date']:

        timed = datetime.utcfromtimestamp(
            int(str(i)[:-3]))
        local = datetime_from_utc_to_local(timed)
        date.append(local)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    trace1 = go.Candlestick(x=date,
                            open=df['open'],
                            high=df['high'],
                            low=df['low'],
                            close=df['close'], name='Цена')
    trace2 = go.Bar(x=date, y=df["volume"],
                    marker=dict(color='rgb(34,163,192)'), name='Объем', opacity=0.7)

    fig.add_trace(trace1)
    fig.add_trace(trace2, secondary_y=True)

    fig.update_xaxes(tickvals=date[::5])
    fig.update_yaxes(showgrid=False)
    fig.update_layout(plot_bgcolor='#e6fbff')

    fig.update_traces(increasing_line_color='#006620',
                      selector=dict(type='candlestick'))
    fig['layout'].update(xaxis=dict(
        tickangle=-90,
    ))

    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.write_image("chart.png")

    print('...ChartGen...')


if __name__ == '__main__':
    chart_gen()
