from time import sleep
import uuid
import streamlit as st
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
"""
This is the main file for the Stock Market Prediction Web App.
It uses the Streamlit library to create a user-friendly web application
that allows users to select a stock, view historical data, and predict future trends using the Prophet library.
"""
from services import load_data, plot_data, plot_multiple_data

# Set page layout to wide
st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Options")
start_date_key = str(uuid.uuid4())
start_date = st.sidebar.date_input("Start date", date(2015, 1, 1), key=start_date_key)
TODAY = date.today().strftime("%Y-%m-%d")

# Header
st.markdown("<h1 style='text-align: center;'>Stock Forecast App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>A simple web app for stock price prediction using the <a href='https://facebook.github.io/prophet/'>Prophet</a> library.</p>", unsafe_allow_html=True)

# Tabs
dataframes_tab, plots_tab, statistics_tab, forecasting_tab, comparison_tab = st.tabs(["Dataframes", "Plots", "Statistics", "Forecasting", "Comparison"])

# Stock selection
stocks = ("AAPL", "GOOG", "MSFT", "GME", "AMC", "TSLA", "FB", "AMZN", "NFLX", "NVDA", "AMD", "PYPL")
selected_stock = st.sidebar.selectbox("Select stock for prediction", stocks)
selected_stocks = st.sidebar.multiselect("Select stocks for comparison", stocks)

years_to_predict = st.sidebar.slider("Years of prediction:", 1, 5)
period = years_to_predict * 365

def load_stock_data(stock, start_date, end_date):
    """
    Load stock data for the specified stock within the given date range.

    Parameters:
    stock (str): The stock ticker symbol to load data for.
    start_date (datetime.date): The start date of the data range.
    end_date (datetime.date): The end date of the data range.

    Returns:
    DataFrame: The loaded stock data.
    """
    with st.spinner("Loading data..."):
        data = load_data(stock, start_date, end_date)
        sleep(1)  # Introducing delay to simulate loading
        return data

# Load data for the selected stock
data = load_stock_data(selected_stock, start_date, TODAY)

# Display the success message
success_message = st.success("Data loaded successfully!")

# Introduce a delay before clearing the success message
sleep(1)

# Clear the success message
success_message.empty()

# Forecasting
df_train = data[["Date", "Close"]]
def forecast_stock(training_data, prediction_period):
    """
    Forecast the stock prices using the Prophet model for the given prediction period.

    Parameters:
    training_data (DataFrame): The historical data to train the model on, with columns 'ds' and 'y'.
    prediction_period (int): The number of periods to predict into the future.

    Returns:
    tuple[model (Prophet), forecast (DataFrame)]: The trained Prophet model and the forecast results.
    """
    model = Prophet()
    model.fit(training_data)
    future = model.make_future_dataframe(periods=prediction_period)
    forecast = model.predict(future)
    forecast = forecast[forecast['ds'] >= TODAY]
    return model, forecast

df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
model, forecast = forecast_stock(df_train, period)

# Dataframes Tab
with dataframes_tab:
    # Display historical data
    st.markdown("<h2><span style='color: orange;'>{}</span> Historical Data</h2>".format(selected_stock), unsafe_allow_html=True)
    st.write("This section displays historical stock price data for {}.".format(selected_stock))
    st.dataframe(data, use_container_width=True)

    # Display forecast data
    st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Data</h2>".format(selected_stock), unsafe_allow_html=True)
    st.write("This section displays the forecasted stock price data for {} using the Prophet model.".format(selected_stock))
    st.dataframe(forecast, use_container_width=True)

# Plots Tab
with plots_tab:
    # Raw data plot
    plot_data(data)

# Statistics Tab
with statistics_tab:
    st.markdown("<h2><span style='color: orange;'>Descriptive </span>Statistics</h2>", unsafe_allow_html=True)
    st.write("This section provides descriptive statistics for the selected stock.")

    # Descriptive Statistics Table
    # drop the date column
    data = data.drop(columns=['Date', 'Adj Close', 'Volume'])
    st.table(data.describe())

# Forecasting Tab
with forecasting_tab:
    # Plotting forecast
    st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Plot</h2>".format(selected_stock), unsafe_allow_html=True)
    st.write("This section visualizes the forecasted stock price for {} using a time series plot.".format(selected_stock))
    forecast_plot = plot_plotly(model, forecast)
    st.plotly_chart(forecast_plot, use_container_width=True)

    # Plotting forecast components
    st.markdown("<h2><span style='color: orange;'>{}</span> Forecast Components</h2>".format(selected_stock), unsafe_allow_html=True)
    st.write("This section breaks down the forecast components, including trends and seasonality, for {}.".format(selected_stock))
    components = model.plot_components(forecast)
    st.write(components)

# Comparison Tab
with comparison_tab:
    if selected_stocks:
        # Forecast multiple stocks
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
    else:
        st.warning("Please select at least one stock if you want to compare them.")

# Display balloons at the end
# st.balloons()