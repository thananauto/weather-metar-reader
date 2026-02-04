from flask import Flask, render_template, request, jsonify
import requests
from metar_decoder import decode_metar

app = Flask(__name__)

METAR_API_URL = "https://aviationweather.gov/api/data/metar"


@app.route('/')
def index():
    """Render the home page with input form."""
    return render_template('index.html')


@app.route('/get-weather', methods=['POST'])
def get_weather():
    """Fetch and decode METAR data for the given airport code."""
    airport_code = request.form.get('airport_code', '').strip().upper()

    if not airport_code:
        return render_template('result.html',
                             error="Please enter an airport code")

    if len(airport_code) != 4:
        return render_template('result.html',
                             error="Airport code must be 4 characters (e.g., VOMM, KJFK)")

    try:
        # Fetch METAR data from API
        response = requests.get(
            METAR_API_URL,
            params={'ids': airport_code},
            timeout=10
        )
        response.raise_for_status()

        metar_raw = response.text.strip()

        if not metar_raw or metar_raw.startswith('No') or metar_raw.startswith('Error'):
            return render_template('result.html',
                                 error=f"No METAR data found for airport code: {airport_code}")

        # Decode METAR
        decoded = decode_metar(metar_raw)

        return render_template('result.html',
                             airport_code=airport_code,
                             raw_metar=metar_raw,
                             decoded=decoded)

    except requests.RequestException as e:
        return render_template('result.html',
                             error=f"Failed to fetch METAR data: {str(e)}")
    except Exception as e:
        return render_template('result.html',
                             error=f"Error decoding METAR: {str(e)}")


@app.route('/api/weather/<airport_code>')
def api_weather(airport_code):
    """API endpoint to get weather data as JSON."""
    airport_code = airport_code.strip().upper()

    try:
        response = requests.get(
            METAR_API_URL,
            params={'ids': airport_code},
            timeout=10
        )
        response.raise_for_status()

        metar_raw = response.text.strip()

        if not metar_raw or metar_raw.startswith('No'):
            return jsonify({'error': 'No METAR data found'}), 404

        decoded = decode_metar(metar_raw)

        return jsonify({
            'airport_code': airport_code,
            'raw_metar': metar_raw,
            'decoded': decoded
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
