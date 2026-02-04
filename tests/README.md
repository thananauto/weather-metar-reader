# METAR Weather Reader - Test Suite Documentation

This directory contains comprehensive unit tests for the METAR Weather Reader application.

## 📋 Test Coverage

The test suite covers all routes and functionality:

### Test Classes

1. **TestIndexRoute** - Home page tests
   - Page loads successfully
   - Form elements are present
   - Example airport codes displayed

2. **TestGetWeatherSuccess** - Successful weather retrieval
   - Valid airport codes (KJFK, VOMM, EGLL)
   - Input normalization (lowercase, whitespace)
   - METAR decoding

3. **TestGetWeatherValidation** - Input validation
   - Empty airport codes
   - Missing parameters
   - Invalid lengths (too short/too long)

4. **TestGetWeatherAPIErrors** - Error handling
   - No METAR data available
   - Network timeouts
   - HTTP errors
   - METAR parsing errors

5. **TestAPIEndpoint** - REST API tests
   - JSON response format
   - Status codes (200, 404, 500)
   - Response structure
   - Error responses

6. **TestEdgeCases** - Edge cases
   - Empty API responses
   - Special characters
   - Numeric airport codes

7. **TestIntegration** - Integration tests
   - Full workflow testing
   - API and web interface consistency

## 🚀 Running Tests

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src/metar_app --cov-report=html
```

### Using the Test Runner Script

```bash
# Full test suite with coverage
./run_tests.sh

# Quick tests (no coverage)
./run_tests.sh quick

# Coverage only
./run_tests.sh coverage
```

### Running Specific Tests

```bash
# Run tests for a specific class
pytest tests/test_app.py::TestIndexRoute -v

# Run a specific test method
pytest tests/test_app.py::TestIndexRoute::test_index_page_loads -v

# Run tests matching a pattern
pytest tests/ -k "valid_airport" -v
```

## 📊 Test Statistics

- **Total Test Cases**: 35+
- **Test Classes**: 7
- **Mock Scenarios**: 3 different METAR conditions
- **Coverage Target**: >90%

## 🧪 Mock Data

The test suite includes comprehensive mock data:

### Airport Codes Tested
- **KJFK** - John F. Kennedy Airport (New York)
- **VOMM** - Chennai International Airport (India)
- **EGLL** - London Heathrow (UK)

### Weather Conditions
1. **Clear Weather** - Few clouds, cold temperature
2. **Hot & Windy** - High temperature, gusty winds
3. **Rainy** - Light rain, low clouds

### Error Scenarios
- No METAR data available
- API errors
- Network timeouts
- Malformed METAR

## 📁 Test Files

```
tests/
├── __init__.py          # Test package initialization
├── test_app.py          # Main test suite for app.py
└── README.md            # This file
```

## 🔧 Configuration Files

- **pytest.ini** - Pytest configuration
- **.coveragerc** - Coverage settings
- **run_tests.sh** - Test runner script

## 📈 Coverage Report

After running tests with coverage, view the HTML report:

```bash
# Generate coverage report
pytest tests/ --cov=src/metar_app --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html

# Open in browser (Linux)
xdg-open htmlcov/index.html

# Open in browser (Windows)
start htmlcov/index.html
```

## 🎯 Testing Best Practices

### Writing New Tests

1. **Follow naming conventions**
   ```python
   def test_descriptive_name():
       # Arrange
       # Act
       # Assert
   ```

2. **Use descriptive assertions**
   ```python
   assert response.status_code == 200, "Expected successful response"
   ```

3. **Mock external dependencies**
   ```python
   @patch('app.requests.get')
   def test_api_call(mock_get):
       mock_get.return_value = Mock()
   ```

4. **Test one thing at a time**
   Each test should verify a single behavior

5. **Use fixtures for common setup**
   ```python
   @pytest.fixture
   def sample_data():
       return {'key': 'value'}
   ```

## 🐛 Debugging Tests

### Running with More Detail

```bash
# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x

# Show full tracebacks
pytest tests/ --tb=long

# Run last failed tests only
pytest tests/ --lf
```

### Using pdb Debugger

```python
def test_something():
    import pdb; pdb.set_trace()
    # Test code here
```

## 🔄 Continuous Integration

The tests are designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ --cov=src/metar_app --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## 📝 Test Maintenance

### When to Update Tests

- ✅ After adding new routes or features
- ✅ After fixing bugs (add test to prevent regression)
- ✅ After changing API behavior
- ✅ When mock data becomes outdated

### Code Coverage Goals

- **Minimum**: 80% coverage
- **Target**: 90% coverage
- **Ideal**: 95%+ coverage

## 🤝 Contributing

When contributing tests:

1. **Write tests for new features**
   Every new feature should have tests

2. **Update existing tests**
   If you change behavior, update tests

3. **Run tests before committing**
   ```bash
   ./run_tests.sh
   ```

4. **Check coverage**
   Ensure new code is tested

## 🆘 Troubleshooting

### Common Issues

#### Import Errors

```bash
# Make sure you're in the project root
cd /path/to/weather-metar-reader

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

#### Mock Not Working

```python
# Correct patch path (module where it's used, not defined)
@patch('app.requests.get')  # ✅ Correct
@patch('requests.get')      # ❌ Wrong
```

#### Fixture Not Found

```python
# Make sure fixture is in the same file or conftest.py
@pytest.fixture
def my_fixture():
    return "value"
```

## 📚 Resources

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py Docs](https://coverage.readthedocs.io/)
- [Flask Testing](https://flask.palletsprojects.com/en/3.0.x/testing/)

---

**Last Updated**: 2026-02-04
**Test Framework**: pytest 7.4.3
**Python Version**: 3.8+
