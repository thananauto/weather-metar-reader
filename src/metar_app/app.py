"""
METAR Weather Reader - Flask Application

This is the main Flask web application that serves the METAR weather reader.
It provides both a web interface and a REST API for accessing decoded METAR data.

METAR (Meteorological Aerodrome Report) is a standardized format for reporting
weather information at airports worldwide. This app fetches real-time METAR data
and translates it into plain English.

Routes:
    /                    - Home page with airport code input form
    /get-weather         - POST endpoint to fetch and display weather
    /api/weather/<code>  - REST API endpoint returning JSON

Example:
    Run the app with: python app.py
    Then visit: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import requests
from metar_decoder import decode_metar

# Initialize Flask application
app = Flask(__name__)

# API endpoint for fetching METAR data from Aviation Weather Center
# Replace 'ids' parameter with any ICAO airport code (e.g., KJFK, VOMM, EGLL)
METAR_API_URL = "https://aviationweather.gov/api/data/metar"


@app.route('/')
def index():
    """
    Home page route.

    Renders the main landing page with an input form where users can
    enter a 4-letter ICAO airport code to get weather information.

    Returns:
        HTML: Rendered index.html template
    """
    return render_template('index.html')


@app.route('/get-weather', methods=['POST'])
def get_weather():
    """
    Fetch and decode METAR weather data for a given airport.

    This endpoint receives form data from the home page, validates the airport
    code, fetches METAR data from the Aviation Weather API, decodes it into
    human-readable format, and displays the results.

    Form Parameters:
        airport_code (str): 4-letter ICAO airport code (e.g., KJFK, VOMM)

    Returns:
        HTML: Rendered result.html with decoded weather data or error message

    Process Flow:
        1. Validate airport code format (must be 4 characters)
        2. Fetch raw METAR from aviationweather.gov API
        3. Decode METAR using the metar_decoder module
        4. Display results in human-readable format
    """
    # Extract and normalize airport code from form submission
    airport_code = request.form.get('airport_code', '').strip().upper()

    # Validation: Check if airport code is provided
    if not airport_code:
        return render_template('result.html',
                             error="Please enter an airport code")

    # Validation: ICAO codes are always 4 characters
    # Examples: KJFK (New York), VOMM (Chennai), EGLL (London)
    if len(airport_code) != 4:
        return render_template('result.html',
                             error="Airport code must be 4 characters (e.g., VOMM, KJFK)")

    try:
        # Fetch raw METAR data from Aviation Weather Center API
        # The API returns plain text METAR observations
        response = requests.get(
            METAR_API_URL,
            params={'ids': airport_code},
            timeout=10  # 10 second timeout to prevent hanging
        )
        response.raise_for_status()  # Raise exception for HTTP errors

        metar_raw = response.text.strip()

        # Check if API returned valid data
        # API returns "No valid METAR..." when airport code is invalid
        if not metar_raw or metar_raw.startswith('No') or metar_raw.startswith('Error'):
            return render_template('result.html',
                                 error=f"No METAR data found for airport code: {airport_code}")

        # Decode the raw METAR string into human-readable format
        # This converts technical aviation codes into plain English
        decoded = decode_metar(metar_raw)

        # Display results with both raw METAR and decoded information
        return render_template('result.html',
                             airport_code=airport_code,
                             raw_metar=metar_raw,
                             decoded=decoded)

    except requests.RequestException as e:
        # Handle network errors (connection timeout, DNS failure, etc.)
        return render_template('result.html',
                             error=f"Failed to fetch METAR data: {str(e)}")
    except Exception as e:
        # Handle METAR parsing errors or other unexpected issues
        return render_template('result.html',
                             error=f"Error decoding METAR: {str(e)}")


@app.route('/api/weather/<airport_code>')
def api_weather(airport_code):
    """
    REST API endpoint for programmatic access to weather data.

    This endpoint allows developers to integrate METAR weather data into their
    own applications. Returns JSON with both raw METAR and decoded data.

    URL Parameters:
        airport_code (str): 4-letter ICAO airport code

    Returns:
        JSON: Weather data object containing:
            - airport_code: The requested airport code
            - raw_metar: Raw METAR observation string
            - decoded: Human-readable weather information
                - summary: Brief weather summary
                - details: List of detailed conditions
                - station: Airport station ID
                - time: Observation time in UTC

    Status Codes:
        200: Success
        404: No METAR data found for airport
        500: Server error (API failure, parsing error, etc.)

    Example:
        GET /api/weather/KJFK
        Response:
        {
            "airport_code": "KJFK",
            "raw_metar": "KJFK 041851Z 31008KT 10SM FEW250...",
            "decoded": {
                "summary": "Clear skies, 25°F, winds 9 mph from the northwest.",
                "details": [...],
                "station": "KJFK",
                "time": "2026-02-04 18:51 UTC"
            }
        }
    """
    # Normalize airport code to uppercase
    airport_code = airport_code.strip().upper()

    try:
        # Fetch METAR data from Aviation Weather API
        response = requests.get(
            METAR_API_URL,
            params={'ids': airport_code},
            timeout=10
        )
        response.raise_for_status()

        metar_raw = response.text.strip()

        # Return 404 if no data found for the airport code
        if not metar_raw or metar_raw.startswith('No'):
            return jsonify({'error': 'No METAR data found'}), 404

        # Decode METAR into human-readable format
        decoded = decode_metar(metar_raw)

        # Return JSON response with all weather data
        return jsonify({
            'airport_code': airport_code,
            'raw_metar': metar_raw,
            'decoded': decoded
        })

    except Exception as e:
        # Return 500 for any server errors
        return jsonify({'error': str(e)}), 500


# Application entry point
# When running this file directly, start the Flask development server
if __name__ == '__main__':
    # Debug mode enabled for development (auto-reload on code changes)
    # Host 0.0.0.0 makes the server accessible from other devices on the network
    # Port 5000 is the default Flask port
    app.run(debug=True, host='0.0.0.0', port=5000)
