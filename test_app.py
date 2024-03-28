import unittest
from unittest.mock import patch

from app import app

class TestWeatherAPI(unittest.TestCase):

    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        # Mock successful response with sample weather data
        mock_response = mock_get.return_value
        mock_response.json.return_value = {'weather': [{'main': 'Clear'}]}

        # Define expected latitude and longitude
        lat = 37.7749
        lon = -122.4194

        # Send a GET request with required parameters
        response = app.test_client().get(f'/weather?lat={lat}&lon={lon}')

        # Assert successful response status code
        self.assertEqual(response.status_code, 200)

        # Assert response data contains weather information
        self.assertIn('weather', response.json)
        self.assertEqual(response.json['weather'][0]['main'], 'Clear')

    @patch('requests.get')
    def test_get_weather_missing_params(self, mock_get):
        # No latitude provided
        response = app.test_client().get('/weather?lon=-122.4194')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

        # No longitude provided
        response = app.test_client().get('/weather?lat=37.7749')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    @patch('requests.get')
    def test_get_weather_api_error(self, mock_get):
        # Mock failed API request (e.g., network error)
        mock_get.side_effect = requests.RequestException('API request failed')

        # Send a GET request
        response = app.test_client().get('/weather?lat=37.7749&lon=-122.4194')

        # Assert internal server error
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json)

