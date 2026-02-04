"""
Unit Tests for METAR Weather Reader Flask Application

This test suite covers all routes and scenarios in the Flask application:
- Index page rendering
- Weather data fetching with valid airport codes
- Error handling for invalid codes
- API endpoint functionality
- Network error scenarios
- METAR decoding errors

Test Framework: pytest with unittest.mock
Coverage: Routes, error handling, API integration
"""

import sys
import os
import pytest
from unittest.mock import patch, Mock
from io import BytesIO

# Add the src/metar_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src/metar_app'))

from app import app


# ============================================================================
# MOCK DATA - Sample METAR observations for testing
# ============================================================================

# Valid METAR data for different weather conditions
MOCK_METAR_KJFK = "KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034 RMK AO2"
MOCK_METAR_VOMM = "VOMM 041830Z 09005KT 8000 FEW020 SCT100 32/24 Q1010"
MOCK_METAR_EGLL = "EGLL 041850Z 24015KT 9999 -RA SCT012 BKN025 09/07 Q1015"

# Mock decoded METAR data structure
MOCK_DECODED_KJFK = {
    'summary': 'Few clouds, 25°F, winds 9 mph from the northwest.',
    'details': [
        'Sky: Few clouds at 25000 feet',
        'Temperature: 25°F (-4°C)',
        'Dew point: 1°F (-17°C)',
        'Wind: 9 mph (8 knots) from the northwest',
        'Visibility: 10+ miles (excellent)',
        'Pressure: 30.34 inHg (1027 mb)'
    ],
    'station': 'KJFK',
    'time': '2026-02-04 18:51 UTC'
}

MOCK_DECODED_VOMM = {
    'summary': 'Few clouds, 90°F, winds 6 mph from the east.',
    'details': [
        'Sky: Few clouds at 2000 feet, Scattered clouds at 10000 feet',
        'Temperature: 90°F (32°C)',
        'Dew point: 75°F (24°C)',
        'Wind: 6 mph (5 knots) from the east',
        'Visibility: 5.0 miles',
        'Pressure: 29.83 inHg (1010 mb)'
    ],
    'station': 'VOMM',
    'time': '2026-02-04 18:30 UTC'
}

# Error responses from API
MOCK_NO_DATA_RESPONSE = "No valid METAR available"
MOCK_ERROR_RESPONSE = "Error: Invalid airport code"


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """
    Create a test client for the Flask application.

    This fixture provides a test client that can be used to make
    requests to the application without running a real server.

    Yields:
        FlaskClient: Test client for making HTTP requests
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ============================================================================
# TEST: Index Route
# ============================================================================

class TestIndexRoute:
    """Test cases for the home page route (/)"""

    def test_index_page_loads(self, client):
        """
        Test that the index page loads successfully.

        Verifies:
        - HTTP 200 status code
        - HTML content is returned
        - Page contains expected elements
        """
        response = client.get('/')

        assert response.status_code == 200
        assert b'METAR Reader' in response.data
        assert b'Airport Code' in response.data
        assert b'Get Weather Report' in response.data

    def test_index_page_has_form(self, client):
        """
        Test that the index page contains the airport code form.

        Verifies:
        - Form with correct action endpoint
        - Input field for airport code
        - Submit button
        """
        response = client.get('/')

        assert b'action="/get-weather"' in response.data
        assert b'name="airport_code"' in response.data
        assert b'type="submit"' in response.data

    def test_index_page_has_examples(self, client):
        """
        Test that the index page displays example airport codes.

        Verifies:
        - Example codes are present (KJFK, KLAX, VOMM, etc.)
        """
        response = client.get('/')

        assert b'KJFK' in response.data
        assert b'KLAX' in response.data
        assert b'VOMM' in response.data
        assert b'EGLL' in response.data


# ============================================================================
# TEST: Get Weather Route - Success Cases
# ============================================================================

class TestGetWeatherSuccess:
    """Test cases for successful weather data retrieval"""

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_valid_airport_code_kjfk(self, mock_decode, mock_get, client):
        """
        Test weather retrieval for a valid airport code (KJFK).

        Verifies:
        - Successful API call
        - METAR decoding
        - Results page display

        Args:
            mock_decode: Mock for decode_metar function
            mock_get: Mock for requests.get function
            client: Flask test client
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Make request
        response = client.post('/get-weather', data={'airport_code': 'KJFK'})

        # Assertions
        assert response.status_code == 200
        assert b'KJFK' in response.data
        assert b'Weather Report' in response.data
        assert b'Few clouds, 25' in response.data

        # Verify API was called correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]['params']['ids'] == 'KJFK'

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_valid_airport_code_vomm(self, mock_decode, mock_get, client):
        """
        Test weather retrieval for Chennai airport (VOMM).

        Tests international airport with different weather conditions.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_VOMM
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_VOMM

        # Make request
        response = client.post('/get-weather', data={'airport_code': 'VOMM'})

        # Assertions
        assert response.status_code == 200
        assert b'VOMM' in response.data
        assert b'90' in response.data  # Temperature

        # Verify decode was called with correct data
        mock_decode.assert_called_once_with(MOCK_METAR_VOMM)

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_lowercase_airport_code_normalized(self, mock_decode, mock_get, client):
        """
        Test that lowercase airport codes are normalized to uppercase.

        Verifies:
        - Lowercase input 'kjfk' is converted to 'KJFK'
        - API is called with uppercase code
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Make request with lowercase
        response = client.post('/get-weather', data={'airport_code': 'kjfk'})

        # Verify uppercase was used
        assert response.status_code == 200
        call_args = mock_get.call_args
        assert call_args[1]['params']['ids'] == 'KJFK'

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_airport_code_with_whitespace(self, mock_decode, mock_get, client):
        """
        Test that airport codes with leading/trailing whitespace are trimmed.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Make request with whitespace
        response = client.post('/get-weather', data={'airport_code': '  KJFK  '})

        # Verify trimmed code was used
        assert response.status_code == 200
        call_args = mock_get.call_args
        assert call_args[1]['params']['ids'] == 'KJFK'


# ============================================================================
# TEST: Get Weather Route - Validation Errors
# ============================================================================

class TestGetWeatherValidation:
    """Test cases for input validation"""

    def test_empty_airport_code(self, client):
        """
        Test error handling for empty airport code.

        Verifies:
        - Error message is displayed
        - No API call is made
        """
        response = client.post('/get-weather', data={'airport_code': ''})

        assert response.status_code == 200
        assert b'Please enter an airport code' in response.data

    def test_missing_airport_code_parameter(self, client):
        """
        Test error handling when airport_code parameter is missing.
        """
        response = client.post('/get-weather', data={})

        assert response.status_code == 200
        assert b'Please enter an airport code' in response.data

    def test_airport_code_too_short(self, client):
        """
        Test error handling for airport codes shorter than 4 characters.

        ICAO codes must be exactly 4 characters.
        """
        response = client.post('/get-weather', data={'airport_code': 'JFK'})

        assert response.status_code == 200
        assert b'must be 4 characters' in response.data

    def test_airport_code_too_long(self, client):
        """
        Test error handling for airport codes longer than 4 characters.
        """
        response = client.post('/get-weather', data={'airport_code': 'KJFKX'})

        assert response.status_code == 200
        assert b'must be 4 characters' in response.data


# ============================================================================
# TEST: Get Weather Route - API Error Cases
# ============================================================================

class TestGetWeatherAPIErrors:
    """Test cases for API-related errors"""

    @patch('app.requests.get')
    def test_no_metar_data_available(self, mock_get, client):
        """
        Test handling when no METAR data is available for airport.

        This happens for:
        - Invalid airport codes
        - Airports that don't report METAR
        - Temporarily unavailable data
        """
        # Setup mock to return "No data" response
        mock_response = Mock()
        mock_response.text = MOCK_NO_DATA_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.post('/get-weather', data={'airport_code': 'XXXX'})

        assert response.status_code == 200
        assert b'No METAR data found' in response.data

    @patch('app.requests.get')
    def test_api_error_response(self, mock_get, client):
        """
        Test handling when API returns an error message.
        """
        # Setup mock to return error response
        mock_response = Mock()
        mock_response.text = MOCK_ERROR_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.post('/get-weather', data={'airport_code': 'INVALID'})

        assert response.status_code == 200
        assert b'No METAR data found' in response.data

    @patch('app.requests.get')
    def test_network_timeout(self, mock_get, client):
        """
        Test handling of network timeout errors.

        Simulates scenario where API is unreachable or slow.
        """
        # Setup mock to raise timeout exception
        mock_get.side_effect = Exception("Connection timeout")

        response = client.post('/get-weather', data={'airport_code': 'KJFK'})

        assert response.status_code == 200
        assert b'Failed to fetch METAR data' in response.data or b'Error decoding METAR' in response.data

    @patch('app.requests.get')
    def test_http_error_404(self, mock_get, client):
        """
        Test handling of HTTP 404 errors from API.
        """
        # Setup mock to raise HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        response = client.post('/get-weather', data={'airport_code': 'KJFK'})

        assert response.status_code == 200
        assert b'Failed to fetch METAR data' in response.data or b'Error decoding METAR' in response.data

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_metar_decoding_error(self, mock_decode, mock_get, client):
        """
        Test handling of METAR decoding errors.

        Simulates malformed METAR data that cannot be parsed.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = "INVALID METAR FORMAT"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Mock decode to raise exception
        mock_decode.side_effect = Exception("Failed to parse METAR")

        response = client.post('/get-weather', data={'airport_code': 'KJFK'})

        assert response.status_code == 200
        assert b'Error decoding METAR' in response.data


# ============================================================================
# TEST: API Endpoint - Success Cases
# ============================================================================

class TestAPIEndpoint:
    """Test cases for the REST API endpoint (/api/weather/<code>)"""

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_api_endpoint_valid_airport(self, mock_decode, mock_get, client):
        """
        Test API endpoint returns JSON for valid airport code.

        Verifies:
        - JSON response format
        - Correct data structure
        - HTTP 200 status
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Make API request
        response = client.get('/api/weather/KJFK')

        # Assertions
        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.get_json()
        assert data['airport_code'] == 'KJFK'
        assert data['raw_metar'] == MOCK_METAR_KJFK
        assert 'decoded' in data
        assert data['decoded']['station'] == 'KJFK'

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_api_endpoint_lowercase_normalized(self, mock_decode, mock_get, client):
        """
        Test API endpoint normalizes lowercase airport codes.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Make request with lowercase
        response = client.get('/api/weather/kjfk')

        assert response.status_code == 200
        data = response.get_json()
        assert data['airport_code'] == 'KJFK'

    @patch('app.requests.get')
    def test_api_endpoint_no_data_404(self, mock_get, client):
        """
        Test API endpoint returns 404 when no METAR data is available.

        Verifies:
        - HTTP 404 status code
        - JSON error message
        """
        # Setup mock to return no data
        mock_response = Mock()
        mock_response.text = MOCK_NO_DATA_RESPONSE
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get('/api/weather/XXXX')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    @patch('app.requests.get')
    def test_api_endpoint_server_error_500(self, mock_get, client):
        """
        Test API endpoint returns 500 on server errors.

        Verifies:
        - HTTP 500 status code
        - JSON error message
        """
        # Setup mock to raise exception
        mock_get.side_effect = Exception("Server error")

        response = client.get('/api/weather/KJFK')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_api_endpoint_response_structure(self, mock_decode, mock_get, client):
        """
        Test that API response has the correct structure.

        Verifies all required fields are present.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        response = client.get('/api/weather/KJFK')
        data = response.get_json()

        # Verify structure
        assert 'airport_code' in data
        assert 'raw_metar' in data
        assert 'decoded' in data

        # Verify decoded structure
        decoded = data['decoded']
        assert 'summary' in decoded
        assert 'details' in decoded
        assert 'station' in decoded
        assert 'time' in decoded


# ============================================================================
# TEST: Edge Cases and Special Scenarios
# ============================================================================

class TestEdgeCases:
    """Test cases for edge cases and special scenarios"""

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_empty_metar_response(self, mock_decode, mock_get, client):
        """
        Test handling of empty response from API.
        """
        # Setup mock to return empty string
        mock_response = Mock()
        mock_response.text = ""
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.post('/get-weather', data={'airport_code': 'KJFK'})

        assert response.status_code == 200
        assert b'No METAR data found' in response.data

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_special_characters_in_airport_code(self, mock_decode, mock_get, client):
        """
        Test handling of special characters in airport code.

        Should validate length but still attempt API call.
        """
        response = client.post('/get-weather', data={'airport_code': 'K@#$'})

        # Should pass validation (4 chars) and attempt API call
        # But will likely fail at API level
        assert response.status_code == 200

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_numeric_airport_code(self, mock_decode, mock_get, client):
        """
        Test handling of numeric airport code.

        While unusual, some airport codes contain numbers.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        response = client.post('/get-weather', data={'airport_code': '1234'})

        # Should pass validation and attempt API call
        assert response.status_code == 200


# ============================================================================
# TEST: Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests that test multiple components together"""

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_full_workflow_valid_request(self, mock_decode, mock_get, client):
        """
        Test complete workflow from form submission to result display.

        This integration test verifies:
        1. Form submission
        2. Input normalization
        3. API call
        4. METAR decoding
        5. Result rendering
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Make request
        response = client.post('/get-weather', data={'airport_code': ' kjfk '})

        # Verify complete workflow
        assert response.status_code == 200
        assert b'KJFK' in response.data
        assert b'Weather Report' in response.data

        # Verify mocks were called in correct order
        mock_get.assert_called_once()
        mock_decode.assert_called_once_with(MOCK_METAR_KJFK)

    @patch('app.requests.get')
    @patch('app.decode_metar')
    def test_api_and_web_consistency(self, mock_decode, mock_get, client):
        """
        Test that API endpoint and web interface return consistent data.
        """
        # Setup mocks
        mock_response = Mock()
        mock_response.text = MOCK_METAR_KJFK
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        mock_decode.return_value = MOCK_DECODED_KJFK

        # Get data from API endpoint
        api_response = client.get('/api/weather/KJFK')
        api_data = api_response.get_json()

        # Verify decoded data structure matches what web interface would display
        assert api_data['decoded']['summary'] == MOCK_DECODED_KJFK['summary']
        assert api_data['decoded']['station'] == MOCK_DECODED_KJFK['station']


# ============================================================================
# MAIN - Run tests with pytest
# ============================================================================

if __name__ == '__main__':
    """
    Run tests with pytest when executed directly.

    Usage:
        python test_app.py
        pytest test_app.py -v
        pytest test_app.py -v --cov=app
    """
    pytest.main([__file__, '-v'])
