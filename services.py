import streamlit as st
from plotly import graph_objs as go
import yfinance as yf


@st.cache_data
def load_data(ticker, start, end):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data


def plot_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.update_layout(title_text="Stock Prices Over Time", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_multiple_data(data, stock_names):
    fig = go.Figure()
    for i, stock_data in enumerate(data):
        fig.add_trace(go.Scatter(x=stock_data['ds'], y=stock_data['yhat'], name=f"yhat - {stock_names[i]}"))
    fig.update_layout(title_text="Stock Prices Over Time", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)
