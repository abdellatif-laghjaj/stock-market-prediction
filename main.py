import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

st.sidebar.title("Options")
start_date = st.sidebar.date_input("Start date", date(2015, 1, 1))
TODAY = date.today().strftime("%Y-%m-%d")

st.markdown("<h1 style='text-align: center;'>Stock Forecast App</h1>", unsafe_allow_html=True)

stocks = ("AAPL", "GOOG", "MSFT", "GME", "AMC", "TSLA", "FB", "AMZN", "NFLX", "NVDA", "AMD", "INTC", "PYPL", "ADBE", "CSCO", "CMCSA", "PEP", "AVGO", "TXN", "QCOM", "TMUS", "COST", "AMGN", "CHTR", "SBUX", "INTU", "ISRG", "AMD", "MU", "ADP", "BKNG", "FISV", "GILD", "MDLZ", "ATVI", "CSX", "VRTX", "REGN", "ILMN", "ADI", "BIIB", "NXPI", "ADSK", "MNST", "LRCX", "JD", "EBAY", "ZM", "KHC", "BIDU", "EXC", "WBA", "MELI", "MRNA", "ORLY", "WDAY", "DOCU", "KLAC", "CTSH", "MAR", "LULU", "ROST", "SNPS", "DXCM", "XEL", "ANSS", "ASML", "SGEN", "IDXX", "CDNS", "NTES", "VRSK", "ALGN", "FAST", "SIRI", "PCAR", "XLNX", "PAYX", "CPRT", "VRSN", "DLTR", "CERN", "INCY", "CHKP", "MXIM", "TCOM", "CDW", "SWKS", "FOXA", "FOX", "ULTA", "NTAP", "CTXS", "MXIM", "KLAC", "CTSH", "MAR", "LULU", "ROST", "SNPS", "DXCM", "XEL", "ANSS", "ASML", "SGEN", "IDXX", "CDNS", "NTES", "VRSK", "ALGN", "FAST", "SIRI", "PCAR", "XLNX", "PAYX", "CPRT", "VRSN", "DLTR", "CERN", "INCY", "CHKP", "MXIM", "TCOM", "CDW")
selected_stock = st.sidebar.selectbox("Select stock for prediction", stocks)
years_to_predict = st.sidebar.slider("Years of prediction:", 1, 5)
period = years_to_predict * 365