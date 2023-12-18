import unittest
from unittest.mock import MagicMock, patch

from main import load_data, plot_data, plot_multiple_data
from prophet import Prophet


class TestMain(unittest.TestCase):

    @patch('main.load_data')
    def test_load_data(self, mock_load_data):
        mock_load_data.return_value = MagicMock()
        result = load_data('AAPL', '2015-01-01', '2022-01-01')
        self.assertIsNotNone(result)

    @patch('main.plot_data')
    def test_plot_data(self, mock_plot_data):
        mock_plot_data.return_value = MagicMock()
        result = plot_data(MagicMock())
        self.assertIsNotNone(result)

    @patch('main.plot_multiple_data')
    def test_plot_multiple_data(self, mock_plot_multiple_data):
        mock_plot_multiple_data.return_value = MagicMock()
        result = plot_multiple_data([MagicMock(), MagicMock()], ['AAPL', 'GOOG'])
        self.assertIsNotNone(result)

    @patch('prophet.Prophet')
    def test_prophet_model(self, mock_prophet):
        mock_prophet.return_value = MagicMock()
        model = Prophet()
        self.assertIsNotNone(model)

if __name__ == '__main__':
    unittest.main()
