#!/usr/bin/env python3
"""
METAR Reader - Test Script

This script tests the METAR fetching and decoding functionality without
starting the full Flask web application. It's useful for:
    - Quick verification that the decoder works correctly
    - Testing before deploying the web app
    - Debugging METAR parsing issues
    - Checking API connectivity

Usage:
    python test_metar.py              # Tests with default airport (KJFK)
    python test_metar.py VOMM         # Tests with specific airport code
    ./test_metar.py EGLL              # Can also be run as executable

The script will:
    1. Fetch live METAR data from aviationweather.gov
    2. Display the raw METAR string
    3. Decode it into human-readable format
    4. Show both summary and detailed breakdown
"""

import sys
import requests


def test_metar_fetch_and_decode(airport_code):
    """
    Test fetching and decoding METAR for a given airport.

    This function performs the complete workflow:
        1. Fetch raw METAR from Aviation Weather API
        2. Parse and decode the METAR string
        3. Display results in a formatted output

    Args:
        airport_code (str): 4-letter ICAO airport code to test

    Returns:
        bool: True if test succeeded, False if it failed
    """

    print(f"\n{'='*60}")
    print(f"Testing METAR Reader for: {airport_code}")
    print(f"{'='*60}\n")

    try:
        # Add the metar_app directory to Python's module search path
        # This allows us to import metar_decoder without installing it as a package
        sys.path.insert(0, 'src/metar_app')
        from metar_decoder import decode_metar

        # Fetch live METAR data from Aviation Weather Center API
        print(f"📡 Fetching METAR data from aviationweather.gov...\n")
        url = f"https://aviationweather.gov/api/data/metar?ids={airport_code}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors (4xx, 5xx)

        metar_raw = response.text.strip()

        # Validate that we got actual METAR data (not an error message)
        if not metar_raw or metar_raw.startswith('No'):
            print(f"❌ No METAR data found for {airport_code}")
            print(f"   This could mean:")
            print(f"   - Invalid airport code")
            print(f"   - Airport doesn't report METAR")
            print(f"   - Data temporarily unavailable")
            return False

        # Display the raw METAR string for reference
        print(f"📄 Raw METAR:")
        print(f"   {metar_raw}\n")

        # Decode the METAR using our decoder module
        print(f"🔄 Decoding METAR...\n")
        decoded = decode_metar(metar_raw)

        # Display formatted results
        print(f"✅ DECODED WEATHER REPORT")
        print(f"{'-'*60}")
        print(f"Airport: {decoded['station']}")
        print(f"Time: {decoded['time']}")
        print(f"\n📝 Summary:")
        print(f"   {decoded['summary']}")
        print(f"\n📊 Details:")
        for detail in decoded['details']:
            print(f"   • {detail}")

        print(f"\n{'='*60}")
        print(f"✅ Test successful!\n")
        return True

    except requests.RequestException as e:
        # Handle network-related errors (connection failed, timeout, etc.)
        print(f"❌ Network error: {e}")
        print(f"   Check your internet connection and try again.")
        return False
    except Exception as e:
        # Handle any other errors (METAR parsing, module import, etc.)
        print(f"❌ Error: {e}")
        print(f"\n   Full traceback:")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    """
    Main entry point for the test script.

    Accepts an optional airport code as a command-line argument.
    If no argument is provided, defaults to KJFK (New York JFK Airport).

    Exit codes:
        0: Test successful
        1: Test failed
    """
    # Get airport code from command line or use default
    # sys.argv[0] is the script name, sys.argv[1] is the first argument
    airport = sys.argv[1] if len(sys.argv) > 1 else "KJFK"

    print("\n🌤️  METAR Weather Reader - Test Script")

    # Run the test
    success = test_metar_fetch_and_decode(airport)

    # Display next steps based on test result
    if success:
        print("💡 Tip: Run './run.sh' to start the web application!")
        print("        Or try: python src/metar_app/app.py")
    else:
        print("\n⚠️  Test failed. Please check your internet connection and try again.")
        print("    Make sure the airport code is valid (4 letters, ICAO format)")

    # Exit with appropriate status code
    # Exit code 0 = success, 1 = failure (used in CI/CD pipelines)
    sys.exit(0 if success else 1)
