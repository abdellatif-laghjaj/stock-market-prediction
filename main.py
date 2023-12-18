from time import sleep
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from services import load_data, plot_data

# Set page layout to wide
st.set_page_config(layout="wide")

st.sidebar.title("Options")
start_date = st.sidebar.date_input("Start date", date(2015, 1, 1))
TODAY = date.today().strftime("%Y-%m-%d")

st.markdown("<h1 style='text-align: center;'>Stock Forecast App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>A simple web app for stock price prediction using the <a href='https://facebook.github.io/prophet/'>Prophet</a> library.</p>", unsafe_allow_html=True)

stocks = ("AAPL", "GOOG", "MSFT", "GME", "AMC", "TSLA", "FB", "AMZN", "NFLX", "NVDA", "AMD", "PYPL")
selected_stock = st.sidebar.selectbox("Select stock for prediction", stocks)
years_to_predict = st.sidebar.slider("Years of prediction:", 1, 5)
period = years_to_predict * 365

# Display a loading spinner while loading data
with st.spinner("Loading data..."):
    data = load_data(selected_stock, start_date, TODAY)
    sleep(1)

# Display the success message
success_message = st.success("Data loaded successfully!")

# Introduce a delay before clearing the success message
sleep(1) 

# Clear the success message
success_message.empty()

# Set the width of the table and figure to 100%
st.subheader(f"{selected_stock} Historical Data")
st.dataframe(data, use_container_width=True)
plot_data(data)

# Forecasting
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forcast = m.predict(future)
forcast = forcast[forcast['ds'] >= TODAY]

st.subheader("Forecast data")
st.dataframe(forcast, use_container_width=True)

fig1 = plot_plotly(m, forcast)
st.plotly_chart(fig1, use_container_width=True)
fig2 = m.plot_components(forcast)
st.write(fig2)