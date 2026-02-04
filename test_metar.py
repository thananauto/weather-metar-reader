#!/usr/bin/env python3
"""
Quick test script to verify METAR decoding functionality.
"""

import sys
import requests


def test_metar_fetch_and_decode(airport_code):
    """Test fetching and decoding METAR for a given airport."""

    print(f"\n{'='*60}")
    print(f"Testing METAR Reader for: {airport_code}")
    print(f"{'='*60}\n")

    try:
        # Add src/metar_app to path
        sys.path.insert(0, 'src/metar_app')
        from metar_decoder import decode_metar

        # Fetch METAR data
        print(f"📡 Fetching METAR data from aviationweather.gov...\n")
        url = f"https://aviationweather.gov/api/data/metar?ids={airport_code}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        metar_raw = response.text.strip()

        if not metar_raw or metar_raw.startswith('No'):
            print(f"❌ No METAR data found for {airport_code}")
            return False

        print(f"📄 Raw METAR:")
        print(f"   {metar_raw}\n")

        # Decode METAR
        print(f"🔄 Decoding METAR...\n")
        decoded = decode_metar(metar_raw)

        # Display results
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
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test with default airport or user-provided code
    airport = sys.argv[1] if len(sys.argv) > 1 else "KJFK"

    print("\n🌤️  METAR Weather Reader - Test Script")

    success = test_metar_fetch_and_decode(airport)

    if success:
        print("💡 Tip: Run './run.sh' to start the web application!")
    else:
        print("\n⚠️  Test failed. Please check your internet connection and try again.")

    sys.exit(0 if success else 1)
