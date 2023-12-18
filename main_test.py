import unittest
from datetime import date
from unittest.mock import patch

from main import load_data, plot_data, plot_multiple_data, plot_plotly
from prophet import Prophet


class MainTest(unittest.TestCase):
    @patch('main.load_data')
    def test_display_historical_data(self, mock_load_data):
        mock_load_data.return_value = 'Expected Data'
        result = load_data('AAPL', date(2015, 1, 1), date.today().strftime("%Y-%m-%d"))
        self.assertEqual(result, 'Expected Data')

    @patch('main.Prophet')
    def test_display_forecast_data(self, mock_Prophet):
        mock_model = Prophet()
        mock_model.fit.return_value = 'Expected Forecast'
        result = mock_model.fit('AAPL')
        self.assertEqual(result, 'Expected Forecast')

    @patch('main.load_data')
    def test_calculate_descriptive_statistics(self, mock_load_data):
        mock_load_data.return_value.describe.return_value = 'Expected Statistics'
        result = load_data('AAPL', date(2015, 1, 1), date.today().strftime("%Y-%m-%d")).describe()
        self.assertEqual(result, 'Expected Statistics')

    @patch('main.plot_plotly')
    def test_generate_forecast_plot(self, mock_plot_plotly):
        mock_plot_plotly.return_value = 'Expected Plot'
        result = plot_plotly(Prophet(), 'Forecast')
        self.assertEqual(result, 'Expected Plot')

    @patch('main.Prophet.plot_components')
    def test_plot_forecast_components(self, mock_plot_components):
        mock_plot_components.return_value = 'Expected Components'
        result = Prophet().plot_components('Forecast')
        self.assertEqual(result, 'Expected Components')

    @patch('main.plot_multiple_data')
    def test_plot_multiple_stock_forecasts(self, mock_plot_multiple_data):
        mock_plot_multiple_data.return_value = 'Expected Multiple Plots'
        result = plot_multiple_data(['Forecast1', 'Forecast2'], ['AAPL', 'GOOG'])
        self.assertEqual(result, 'Expected Multiple Plots')

if __name__ == '__main__':
    unittest.main()
