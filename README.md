# METAR Weather Reader ✈️ 🌤️

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A Flask web application that fetches and decodes METAR (Meteorological Aerodrome Report) data into human-readable weather reports. Perfect for pilots, aviation enthusiasts, and anyone who needs quick weather information for airports worldwide.

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Standard Installation](#standard-installation)
  - [Docker Installation](#docker-installation)
- [Usage](#-usage)
  - [Web Interface](#web-interface)
  - [API Endpoint](#api-endpoint)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [How METAR Decoding Works](#-how-metar-decoding-works)
- [Best Practices](#-best-practices)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 🌍 **Global Coverage**: Access real-time METAR data for airports worldwide
- 🔄 **Live Updates**: Fetches current METAR from aviationweather.gov API
- 📖 **Human-Readable**: Converts technical METAR codes into plain English
- 🎨 **Modern UI**: Clean, responsive web interface with gradient design
- 🔌 **REST API**: JSON endpoint for programmatic access
- 🐳 **Docker Ready**: Easy deployment with Docker and docker-compose
- 📊 **Comprehensive Data**: Displays all weather parameters
  - Sky conditions (clear, cloudy, overcast)
  - Temperature in both Fahrenheit and Celsius
  - Wind speed and direction in mph/knots
  - Visibility in statute miles
  - Atmospheric pressure (inHg/mb)
  - Weather phenomena (rain, snow, fog, etc.)

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/thananauto/weather-metar-reader.git
cd weather-metar-reader

# Start with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:5000
```

### Using Python

```bash
# Clone the repository
git clone https://github.com/thananauto/weather-metar-reader.git
cd weather-metar-reader

# Run the convenience script
./run.sh

# Or manually
pip install -r requirements.txt
cd src/metar_app
python app.py
```

## 📦 Installation

### Standard Installation

#### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for API access)

#### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thananauto/weather-metar-reader.git
   cd weather-metar-reader
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv

   # On macOS/Linux
   source venv/bin/activate

   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the installation**
   ```bash
   python test_metar.py KJFK
   ```

5. **Run the application**
   ```bash
   cd src/metar_app
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Installation

#### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+ (optional, for docker-compose method)

#### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/thananauto/weather-metar-reader.git
cd weather-metar-reader

# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

#### Option 2: Docker CLI

```bash
# Build the image
docker build -t metar-weather-reader .

# Run the container
docker run -d \
  --name metar-reader \
  -p 5000:5000 \
  --restart unless-stopped \
  metar-weather-reader

# View logs
docker logs -f metar-reader

# Stop the container
docker stop metar-reader
docker rm metar-reader
```

#### Docker Environment Variables

You can customize the application behavior with environment variables:

```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e PYTHONUNBUFFERED=1 \
  metar-weather-reader
```

## 📖 Usage

### Web Interface

1. **Navigate to the application**
   Open your browser to `http://localhost:5000`

2. **Enter airport code**
   Type a 4-letter ICAO airport code (e.g., `KJFK`, `VOMM`, `EGLL`)

3. **Get weather report**
   Click "Get Weather Report" button

4. **View results**
   See human-readable weather summary and detailed conditions

### API Endpoint

Access weather data programmatically via the REST API.

#### Endpoint

```
GET /api/weather/<airport_code>
```

#### Request Example

```bash
curl http://localhost:5000/api/weather/KJFK
```

#### Response Example

```json
{
  "airport_code": "KJFK",
  "raw_metar": "KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034 RMK AO2 SLP272 T10441172",
  "decoded": {
    "summary": "Few clouds, 25°F, winds 9 mph from the northwest.",
    "details": [
      "Sky: Few clouds at 25000 feet",
      "Temperature: 25°F (-4°C)",
      "Dew point: 1°F (-17°C)",
      "Wind: 9 mph (8 knots) from the northwest",
      "Visibility: 10+ miles (excellent)",
      "Pressure: 30.34 inHg (1027 mb)"
    ],
    "station": "KJFK",
    "time": "2026-02-04 18:51 UTC"
  }
}
```

#### Status Codes

- `200`: Success - Weather data retrieved
- `404`: Not Found - No METAR data for airport code
- `500`: Server Error - API failure or parsing error

#### Using with Programming Languages

**Python:**
```python
import requests

response = requests.get('http://localhost:5000/api/weather/KJFK')
data = response.json()
print(data['decoded']['summary'])
```

**JavaScript:**
```javascript
fetch('http://localhost:5000/api/weather/KJFK')
  .then(response => response.json())
  .then(data => console.log(data.decoded.summary));
```

**curl with jq:**
```bash
curl -s http://localhost:5000/api/weather/KJFK | jq '.decoded.summary'
```

## 🌍 Examples

### Example Airport Codes

| Code | Airport | Location | Region |
|------|---------|----------|--------|
| **KJFK** | John F. Kennedy International | New York, USA | North America |
| **KLAX** | Los Angeles International | Los Angeles, USA | North America |
| **VOMM** | Chennai International | Chennai, India | Asia |
| **EGLL** | London Heathrow | London, UK | Europe |
| **RJTT** | Tokyo Haneda | Tokyo, Japan | Asia |
| **YSSY** | Sydney Kingsford Smith | Sydney, Australia | Oceania |
| **EDDF** | Frankfurt Airport | Frankfurt, Germany | Europe |
| **ZBAA** | Beijing Capital International | Beijing, China | Asia |
| **OMDB** | Dubai International | Dubai, UAE | Middle East |
| **SBGR** | São Paulo/Guarulhos | São Paulo, Brazil | South America |

Find more airport codes: [World Airport Codes](https://www.world-airport-codes.com/)

### Example Outputs

#### Example 1: Clear Weather

**Airport:** KJFK (New York JFK)

**Raw METAR:**
```
KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034
```

**Decoded Summary:**
```
Few clouds, 25°F, winds 9 mph from the northwest.
```

**Detailed Conditions:**
- Sky: Few clouds at 25,000 feet
- Temperature: 25°F (-4°C)
- Dew point: 1°F (-17°C)
- Wind: 9 mph (8 knots) from the northwest
- Visibility: 10+ miles (excellent)
- Pressure: 30.34 inHg (1027 mb)

#### Example 2: Rainy Weather

**Airport:** EGLL (London Heathrow)

**Raw METAR:**
```
EGLL 041850Z 24015KT 9999 -RA SCT012 BKN025 09/07 Q1015
```

**Decoded Summary:**
```
Partly cloudy, 48°F, winds 17 mph from the southwest, light rain.
```

**Detailed Conditions:**
- Sky: Scattered clouds at 1,200 feet, Broken clouds at 2,500 feet
- Temperature: 48°F (9°C)
- Dew point: 45°F (7°C)
- Wind: 17 mph (15 knots) from the southwest
- Visibility: 6+ miles
- Pressure: 29.97 inHg (1015 mb)
- Weather: Light rain

#### Example 3: Windy Conditions

**Airport:** VOMM (Chennai)

**Raw METAR:**
```
VOMM 041830Z 31025G35KT 8000 FEW020 SCT100 32/24 Q1010
```

**Decoded Summary:**
```
Few clouds, 90°F, winds 29 mph from the northwest, gusting to 40 mph.
```

**Detailed Conditions:**
- Sky: Few clouds at 2,000 feet, Scattered clouds at 10,000 feet
- Temperature: 90°F (32°C)
- Dew point: 75°F (24°C)
- Wind: 29 mph (25 knots) from the northwest, gusting to 40 mph (35 knots)
- Visibility: 5.0 miles
- Pressure: 29.83 inHg (1010 mb)

## 📁 Project Structure

```
weather-metar-reader/
├── src/
│   └── metar_app/
│       ├── app.py              # Main Flask application
│       ├── metar_decoder.py    # METAR parsing and decoding logic
│       └── templates/
│           ├── index.html      # Home page with input form
│           └── result.html     # Results page with weather report
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore              # Docker build exclusions
├── requirements.txt            # Python dependencies
├── run.sh                      # Convenience script to run the app
├── test_metar.py              # Test script for validation
├── .gitignore                 # Git exclusions
└── README.md                  # This file
```

## 🔍 How METAR Decoding Works

METAR (Meteorological Aerodrome Report) is a standardized format used worldwide for aviation weather reports. This application uses the `python-metar` library to parse these reports.

### METAR Format Breakdown

**Example METAR:**
```
KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034
```

**Component Breakdown:**

| Component | Code | Meaning |
|-----------|------|---------|
| **Station** | `KJFK` | Airport ICAO code (JFK Airport) |
| **Date/Time** | `041851Z` | 4th day, 18:51 UTC (Z = Zulu time) |
| **Wind** | `31008KT` | 310° at 8 knots |
| **Visibility** | `10SM` | 10 statute miles |
| **Clouds** | `FEW250` | Few clouds at 25,000 feet |
| **Temperature** | `M04` | -4°C (M = minus) |
| **Dew Point** | `M17` | -17°C |
| **Pressure** | `A3034` | 30.34 inches of mercury |

### Common METAR Codes

#### Sky Conditions
- `SKC/CLR`: Clear skies
- `FEW`: Few clouds (1-2 oktas)
- `SCT`: Scattered clouds (3-4 oktas)
- `BKN`: Broken clouds (5-7 oktas)
- `OVC`: Overcast (8 oktas)

#### Weather Phenomena
- `RA`: Rain
- `SN`: Snow
- `FG`: Fog
- `BR`: Mist
- `TS`: Thunderstorm
- `DZ`: Drizzle
- `-`: Light intensity (prefix)
- `+`: Heavy intensity (prefix)

#### Wind
- `00000KT`: Calm
- `VRB`: Variable direction
- `G`: Gust indicator
- Example: `31015G25KT` = 310° at 15kt gusting to 25kt

## ✅ Best Practices

### Development Best Practices

1. **Use Virtual Environments**
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   ```

2. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade -r requirements.txt
   ```

3. **Run Tests Before Commits**
   ```bash
   python test_metar.py KJFK
   python test_metar.py VOMM
   python test_metar.py EGLL
   ```

4. **Use Environment Variables**
   Never hardcode sensitive data. Use environment variables:
   ```python
   import os
   API_KEY = os.getenv('API_KEY', 'default_value')
   ```

5. **Code Documentation**
   All functions include docstrings with examples

### Production Best Practices

1. **Use a Production WSGI Server**

   Don't use Flask's development server in production. Use Gunicorn:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Enable HTTPS**

   Use a reverse proxy (nginx) with SSL certificates:

   ```nginx
   server {
       listen 443 ssl;
       server_name your-domain.com;

       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       location / {
           proxy_pass http://localhost:5000;
       }
   }
   ```

3. **Implement Rate Limiting**

   Protect your API from abuse:

   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

4. **Add Monitoring**

   Use tools like Prometheus, Grafana, or Sentry for monitoring

5. **Implement Caching**

   Cache METAR data (typically valid for 30-60 minutes):

   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})

   @cache.cached(timeout=1800)  # 30 minutes
   def get_metar(airport_code):
       # Fetch METAR
   ```

6. **Security Headers**

   Add security headers to responses:

   ```python
   @app.after_request
   def add_security_headers(response):
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'DENY'
       response.headers['X-XSS-Protection'] = '1; mode=block'
       return response
   ```

### Docker Best Practices

1. **Multi-Stage Builds** ✅
   Already implemented in Dockerfile

2. **Non-Root User** ✅
   Container runs as user `appuser` (UID 1000)

3. **Health Checks** ✅
   Container includes health check endpoint

4. **Small Image Size**
   Using `python:3.11-slim` instead of full Python image

5. **Layer Caching**
   Copy `requirements.txt` before code for better caching

## 🚀 Deployment

### Deploy to Render

1. **Fork this repository**

2. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd src/metar_app && gunicorn app:app`

3. **Set Environment Variables**
   ```
   PYTHON_VERSION=3.11.0
   ```

### Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Deploy to Fly.io

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy**
   ```bash
   fly launch
   fly deploy
   ```

### Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create metar-weather-reader

# Deploy
git push heroku main

# Open app
heroku open
```

### Deploy with Docker on VPS

```bash
# SSH to your server
ssh user@your-server.com

# Clone repository
git clone https://github.com/thananauto/weather-metar-reader.git
cd weather-metar-reader

# Run with docker-compose
docker-compose up -d

# Setup nginx reverse proxy (optional)
sudo apt install nginx
# Configure nginx as reverse proxy to port 5000
```

## 🔧 Troubleshooting

### Common Issues

#### Issue: "No METAR data found"

**Cause:** Invalid airport code or no current METAR available

**Solution:**
- Verify the airport code is correct (4 letters, ICAO format)
- Try another airport code
- Check if the airport reports METAR (small airports may not)

#### Issue: "Failed to fetch METAR data"

**Cause:** Network connectivity issue or API unavailable

**Solution:**
- Check your internet connection
- Verify aviationweather.gov is accessible
- Check firewall settings

#### Issue: "Module not found" errors

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue: Docker container won't start

**Cause:** Port 5000 already in use

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Change port in docker-compose.yml
ports:
  - "8080:5000"  # Use port 8080 instead
```

#### Issue: Docker build fails

**Cause:** Permission issues or network problems

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

### Debug Mode

Enable debug mode for detailed error messages:

```python
# In app.py
app.run(debug=True, host='0.0.0.0', port=5000)
```

⚠️ **Warning:** Never enable debug mode in production!

### Getting Help

- **Check Logs**
  ```bash
  # Docker
  docker-compose logs -f

  # Standard installation
  # Errors will appear in terminal
  ```

- **Test METAR Decoder**
  ```bash
  python test_metar.py KJFK
  ```

- **Open an Issue**
  If you encounter a bug, [open an issue](https://github.com/thananauto/weather-metar-reader/issues) with:
  - Error message
  - Steps to reproduce
  - Your environment (OS, Python version, etc.)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

Open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

### Suggesting Features

Open an issue with:
- Feature description
- Use case
- Proposed implementation (if applicable)

### Submitting Pull Requests

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Add tests if applicable
   - Update documentation
   - Follow existing code style

4. **Test your changes**
   ```bash
   python test_metar.py KJFK
   ```

5. **Commit with clear message**
   ```bash
   git commit -m "Add: Brief description of your change"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2026 thananauto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- [Aviation Weather Center](https://aviationweather.gov/) for providing free METAR data API
- [python-metar](https://github.com/python-metar/python-metar) library for METAR parsing
- Flask community for excellent documentation
- All contributors who help improve this project

## 📞 Support

- **Documentation**: You're reading it! 📖
- **Issues**: [GitHub Issues](https://github.com/thananauto/weather-metar-reader/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thananauto/weather-metar-reader/discussions)

---

**Made with ❤️ by [thananauto](https://github.com/thananauto)**

**Powered by Flask • Python • Aviation Weather Center API**
