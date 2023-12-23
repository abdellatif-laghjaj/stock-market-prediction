import streamlit as st
from plotly import graph_objs as go
import yfinance as yf

@st.cache_data
def load_data(ticker, start, end):
    """
    Load historical stock price data from Yahoo Finance.

    Parameters:
    - ticker (str): Stock symbol (e.g., AAPL).
    - start (str): Start date in the format 'YYYY-MM-DD'.
    - end (str): End date in the format 'YYYY-MM-DD'.

    Returns:
    - data (pd.DataFrame): DataFrame containing historical stock price data.
    """
    try:
        data = yf.download(ticker, start, end)
        data.reset_index(inplace=True)
        return data
    except Exception as e:
        st.error(f"Error loading data for {ticker}: {str(e)}")
        return None

def plot_data(data):
    """
    Plot historical stock price data.

    Parameters:
    - data (pd.DataFrame): DataFrame containing historical stock price data.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.update_layout(title_text="Stock Prices Over Time", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_multiple_data(data, stock_names):
    """
    Plot forecasted stock prices for multiple stocks.

    Parameters:
    - data (list): List of DataFrames containing forecasted stock price data.
    - stock_names (list): List of stock names corresponding to the forecasted data.
    """
    fig = go.Figure()
    for i, stock_data in enumerate(data):
        fig.add_trace(go.Scatter(x=stock_data['ds'], y=stock_data['yhat'], name=f"yhat - {stock_names[i]}"))
    fig.update_layout(title_text="Stock Prices Over Time", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)

def plot_volume(data):
    """
    Plot historical stock volume data.

    Parameters:
    - data (pd.DataFrame): DataFrame containing historical stock volume data.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name="stock_volume"))
    fig.update_layout(title_text="Stock Volume Over Time", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig, use_container_width=True)