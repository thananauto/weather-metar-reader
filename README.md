# METAR Weather Reader

A Flask web application that fetches and decodes METAR (Meteorological Aerodrome Report) data into human-readable weather reports.

## Features

- Enter any airport ICAO code (e.g., KJFK, VOMM, EGLL)
- Fetches real-time METAR data from aviationweather.gov
- Decodes technical METAR format into friendly, readable descriptions
- Shows detailed weather conditions including:
  - Sky conditions (clear, cloudy, overcast)
  - Temperature in Fahrenheit and Celsius
  - Wind speed and direction in plain English
  - Visibility
  - Atmospheric pressure
  - Weather phenomena (rain, snow, etc.)
- Clean, modern web interface
- REST API endpoint for programmatic access

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Using the run script
```bash
./run.sh
```

### Option 2: Manual start
```bash
cd src/metar_app
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Web Interface
1. Open your browser to `http://localhost:5000`
2. Enter a 4-letter ICAO airport code (e.g., KJFK for JFK Airport)
3. Click "Get Weather Report"
4. View the human-readable weather report

### API Endpoint
You can also access weather data programmatically:

```bash
curl http://localhost:5000/api/weather/KJFK
```

Returns JSON with raw METAR and decoded data.

## Example Airport Codes

- **KJFK** - John F. Kennedy International Airport (New York)
- **KLAX** - Los Angeles International Airport
- **VOMM** - Chennai International Airport (India)
- **EGLL** - London Heathrow Airport (UK)
- **RJTT** - Tokyo Haneda Airport (Japan)
- **YSSY** - Sydney Airport (Australia)
- **EDDF** - Frankfurt Airport (Germany)

Find more airport codes at: https://www.world-airport-codes.com/

## How METAR Decoding Works

The application uses the `python-metar` library to parse standardized METAR reports and converts them into natural language. For example:

**Raw METAR:**
```
KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034
```

**Decoded:**
```
Few clouds, 25°F, winds 9 mph from the northwest.
```

## Project Structure

```
├── src/metar_app/
│   ├── app.py              # Main Flask application
│   ├── metar_decoder.py    # METAR parsing and decoding logic
│   └── templates/
│       ├── index.html      # Home page with input form
│       └── result.html     # Results page with weather report
├── requirements.txt        # Python dependencies
├── run.sh                  # Convenience script to run the app
└── README.md              # This file
```

## Dependencies

- **Flask**: Web framework
- **requests**: HTTP library for API calls
- **python-metar**: METAR parsing library

## License

MIT
