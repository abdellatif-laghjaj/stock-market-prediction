from time import sleep
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from services import load_data, plot_raw_data

# Set page layout to wide
st.set_page_config(layout="wide")

st.sidebar.title("Options")
start_date = st.sidebar.date_input("Start date", date(2015, 1, 1))
TODAY = date.today().strftime("%Y-%m-%d")

st.markdown("<h1 style='text-align: center;'>Stock Forecast App</h1>", unsafe_allow_html=True)

stocks = ("AAPL", "GOOG", "MSFT", "GME", "AMC", "TSLA", "FB", "AMZN", "NFLX", "NVDA", "AMD", "INTC", "PYPL", "ADBE", "CSCO", "CMCSA", "PEP", "AVGO", "TXN", "QCOM", "TMUS", "COST", "AMGN", "CHTR", "SBUX", "INTU", "ISRG", "AMD", "MU", "ADP", "BKNG", "FISV", "GILD", "MDLZ", "ATVI", "CSX", "VRTX", "REGN", "ILMN", "ADI", "BIIB", "NXPI", "ADSK", "MNST", "LRCX", "JD", "EBAY", "ZM", "KHC", "BIDU", "EXC", "WBA", "MELI", "MRNA", "ORLY", "WDAY", "DOCU", "KLAC", "CTSH", "MAR", "LULU", "ROST", "SNPS", "DXCM", "XEL", "ANSS", "ASML", "SGEN", "IDXX", "CDNS", "NTES", "VRSK", "ALGN", "FAST", "SIRI", "PCAR", "XLNX", "PAYX", "CPRT", "VRSN", "DLTR", "CERN", "INCY", "CHKP", "MXIM", "TCOM", "CDW", "SWKS", "FOXA", "FOX", "ULTA", "NTAP", "CTXS", "MXIM", "KLAC", "CTSH", "MAR", "LULU", "ROST", "SNPS", "DXCM", "XEL", "ANSS", "ASML", "SGEN", "IDXX", "CDNS", "NTES", "VRSK", "ALGN", "FAST", "SIRI", "PCAR", "XLNX", "PAYX", "CPRT", "VRSN", "DLTR", "CERN", "INCY", "CHKP", "MXIM", "TCOM", "CDW")
selected_stock = st.sidebar.selectbox("Select stock for prediction", stocks)
years_to_predict = st.sidebar.slider("Years of prediction:", 1, 5)
period = years_to_predict * 365

data_load_state = st.progress(0,text="Loading data...")
data = load_data(selected_stock, start_date, TODAY)
data_load_state.progress(100)
data_load_state.text("Data loaded successfully!")
# st.success("Data loaded successfully!")
st.subheader("Raw data")
st.write(data)
plot_raw_data(data)

# Forecasting
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forcast = m.predict(future)
forcast = forcast[forcast['ds'] >= TODAY]

st.subheader("Forcast data")
# get ony forcasted data from today
st.write(forcast)

fig1 = plot_plotly(m,forcast)
st.plotly_chart(fig1)
fig2=m.plot_components(forcast)
st.write(fig2)