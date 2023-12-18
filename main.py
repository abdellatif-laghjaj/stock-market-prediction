from time import sleep
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from services import load_data, plot_data, plot_multiple_data

# Set page layout to wide
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.image("./src/logo.png", width=100)
st.sidebar.title("Options")
start_date = st.sidebar.date_input("Start date", date(2015, 1, 1))
TODAY = date.today().strftime("%Y-%m-%d")

st.markdown("<h1 style='text-align: center;'>Stock Forecast App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>A simple web app for stock price prediction using the <a href='https://facebook.github.io/prophet/'>Prophet</a> library.</p>", unsafe_allow_html=True)

stocks = ("AAPL", "GOOG", "MSFT", "GME", "AMC", "TSLA", "FB", "AMZN", "NFLX", "NVDA", "AMD", "PYPL")
selected_stock = st.sidebar.selectbox("Select stock for prediction", stocks)
selected_stocks = st.sidebar.multiselect("Select stocks for comparaison", stocks)

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
st.markdown("<h2><span style='color: orange;'>{}</span> Historical Data</h2>".format(selected_stock), unsafe_allow_html=True)
st.write("This section displays historical stock price data for {}.".format(selected_stock))
st.dataframe(data, use_container_width=True)
plot_data(data)

# Forecasting
df_train = data[["Date", "Close"]]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
model = Prophet()
model.fit(df_train)
future = model.make_future_dataframe(periods=period)
forecast = model.predict(future)
forecast = forecast[forecast['ds'] >= TODAY]

st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Data</h2>".format(selected_stock), unsafe_allow_html=True)
st.write("This section displays the forecasted stock price data for {} using the Prophet model.".format(selected_stock))
st.dataframe(forecast, use_container_width=True)

# Plotting
st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Plot</h2>".format(selected_stock), unsafe_allow_html=True)
st.write("This section visualizes the forecasted stock price for {} using a time series plot.".format(selected_stock))
forecast_plot = plot_plotly(model, forecast)
st.plotly_chart(forecast_plot, use_container_width=True)

# Plotting components
st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Components</h2>".format(selected_stock), unsafe_allow_html=True)
st.write("This section breaks down the forecast components, including trends and seasonality, for {}.".format(selected_stock))
components = model.plot_components(forecast)
st.write(components)

# Forcast multiple stocks
stocks_data = []
forcasted_data = []
for stock in selected_stocks:
    stocks_data.append(load_data(stock, start_date, TODAY))

st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Plot of Multiple Stocks</h2>".format(', '.join(selected_stocks)), unsafe_allow_html=True)
st.write("This section visualizes the forecasted stock price for {} using a time series plot.".format(', '.join(selected_stocks)))

for data in stocks_data:
    if data is not None:
        df_train = data[["Date", "Close"]]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
        model = Prophet()
        model.fit(df_train)
        future = model.make_future_dataframe(periods=period)
        forecast = model.predict(future)
        forecast = forecast[forecast['ds'] >= TODAY]
        forcasted_data.append(forecast)

plot_multiple_data(forcasted_data, selected_stocks)