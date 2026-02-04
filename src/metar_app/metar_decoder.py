"""
METAR Decoder Module

This module provides functionality to decode METAR (Meteorological Aerodrome Report)
observations into human-readable weather descriptions.

METAR Format Overview:
    METAR is a standardized format used worldwide for aviation weather reports.
    Example: "KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034"

    Components:
        - KJFK: Airport ICAO code
        - 041851Z: Date/Time (4th day, 18:51 UTC)
        - 31008KT: Wind (310 degrees at 8 knots)
        - 10SM: Visibility (10 statute miles)
        - FEW250: Sky condition (few clouds at 25,000 feet)
        - M04/M17: Temperature/Dew point (-4°C / -17°C, M = minus)
        - A3034: Altimeter setting (30.34 inHg)

This module translates these technical codes into natural language descriptions
like "Clear skies, 25°F, winds 9 mph from the northwest."

Dependencies:
    - python-metar: Library for parsing METAR strings
"""

from metar.Metar import Metar


def decode_metar(metar_string):
    """
    Decode a METAR string into human-readable format.

    Takes a raw METAR observation string and parses it into individual
    weather components, then translates each component into plain English.

    Args:
        metar_string (str): Raw METAR observation string
            Example: "KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034"

    Returns:
        dict: Decoded weather information with the following keys:
            - summary (str): Brief one-sentence weather description
            - details (list): Detailed breakdown of all conditions
            - station (str): Airport ICAO code
            - time (str): Observation time in UTC

    Raises:
        Exception: If METAR string cannot be parsed

    Example:
        >>> decode_metar("KJFK 041851Z 31008KT 10SM FEW250 M04/M17 A3034")
        {
            'summary': 'Few clouds, 25°F, winds 9 mph from the northwest.',
            'details': ['Sky: Few clouds at 25000 feet', 'Temperature: 25°F (-4°C)', ...],
            'station': 'KJFK',
            'time': '2026-02-04 18:51 UTC'
        }
    """
    try:
        # Parse METAR string using python-metar library
        # This extracts structured data from the coded format
        obs = Metar(metar_string)

        # Build detailed human-readable descriptions
        # Each function below handles a specific weather component
        description_parts = []

        # Sky conditions (clear, cloudy, overcast, etc.)
        # METAR codes: CLR, FEW, SCT, BKN, OVC with cloud heights
        sky_condition = get_sky_condition(obs)
        if sky_condition:
            description_parts.append(sky_condition)

        # Temperature in both Fahrenheit and Celsius
        # METAR format: Two digits or M## for below zero (M = minus)
        if obs.temp:
            temp_c = obs.temp.value()
            temp_f = (temp_c * 9/5) + 32  # Convert Celsius to Fahrenheit
            description_parts.append(f"Temperature: {temp_f:.0f}°F ({temp_c:.0f}°C)")

        # Dew point (temperature at which air becomes saturated)
        # Important for calculating humidity and fog potential
        if obs.dewpt:
            dewpt_c = obs.dewpt.value()
            dewpt_f = (dewpt_c * 9/5) + 32  # Convert Celsius to Fahrenheit
            description_parts.append(f"Dew point: {dewpt_f:.0f}°F ({dewpt_c:.0f}°C)")

        # Wind speed and direction
        # METAR format: 31008KT = 310 degrees at 8 knots
        wind_info = get_wind_info(obs)
        if wind_info:
            description_parts.append(wind_info)

        # Visibility in statute miles
        # METAR codes: 10SM (10+ miles), lower values indicate fog/haze
        if obs.vis:
            vis_miles = obs.vis.value("SM")
            if vis_miles >= 10:
                description_parts.append(f"Visibility: {vis_miles:.0f}+ miles (excellent)")
            else:
                description_parts.append(f"Visibility: {vis_miles:.1f} miles")

        # Atmospheric pressure (altimeter setting)
        # Used by pilots to calibrate altimeters
        # METAR format: A#### (inHg) or Q#### (hPa/mb)
        if obs.press:
            pressure_mb = obs.press.value()
            pressure_inhg = pressure_mb * 0.02953  # Convert millibars to inches of mercury
            description_parts.append(f"Pressure: {pressure_inhg:.2f} inHg ({pressure_mb:.0f} mb)")

        # Weather phenomena (rain, snow, fog, thunderstorms, etc.)
        # METAR uses codes like RA (rain), SN (snow), FG (fog)
        weather = get_weather_phenomena(obs)
        if weather:
            description_parts.append(weather)

        # Create a friendly one-sentence summary for quick reading
        summary = create_summary(obs)

        # Return structured data with both summary and detailed breakdown
        return {
            'summary': summary,
            'details': description_parts,
            'station': obs.station_id,
            'time': obs.time.strftime('%Y-%m-%d %H:%M UTC') if obs.time else 'Unknown'
        }

    except Exception as e:
        # Re-raise with more context about the failure
        raise Exception(f"Failed to parse METAR: {str(e)}")


def get_sky_condition(obs):
    """
    Decode sky condition and cloud coverage.

    METAR Sky Condition Codes:
        CLR/SKC: Clear skies (0 oktas coverage)
        FEW: Few clouds (1-2 oktas, 12.5-25% coverage)
        SCT: Scattered clouds (3-4 oktas, 37.5-50% coverage)
        BKN: Broken clouds (5-7 oktas, 62.5-87.5% coverage)
        OVC: Overcast (8 oktas, 100% coverage)
        VV: Vertical visibility (used in fog/obscuration)

    Cloud heights are reported in hundreds of feet above ground level.
    Example: FEW250 = few clouds at 25,000 feet

    Args:
        obs (Metar): Parsed METAR observation object

    Returns:
        str: Human-readable sky condition description or None
    """
    if not obs.sky:
        return "Sky condition: Clear"

    conditions = []
    # Iterate through all cloud layers (METAR can report multiple layers)
    for sky in obs.sky:
        cover = sky[0]  # Cloud coverage code (CLR, FEW, SCT, BKN, OVC)
        height = sky[1].value("FT") if sky[1] else None  # Height in feet AGL

        # Translate METAR codes to plain English
        cover_desc = {
            'CLR': 'Clear',           # Clear below 12,000 feet
            'SKC': 'Clear',           # Sky clear (no clouds detected)
            'FEW': 'Few clouds',      # 1-2 oktas coverage
            'SCT': 'Scattered clouds', # 3-4 oktas coverage
            'BKN': 'Broken clouds',   # 5-7 oktas coverage
            'OVC': 'Overcast',        # 8 oktas (complete coverage)
            'VV': 'Vertical visibility' # Obscured sky (fog, etc.)
        }.get(cover, cover)

        # Include height if available
        if height:
            conditions.append(f"{cover_desc} at {height:.0f} feet")
        else:
            conditions.append(cover_desc)

    return "Sky: " + ", ".join(conditions) if conditions else None


def get_wind_info(obs):
    """
    Decode wind speed, direction, and gusts.

    METAR Wind Format:
        31008KT = 310 degrees at 8 knots
        VRB05KT = Variable direction at 5 knots
        31008G15KT = 310° at 8kt gusting to 15kt
        00000KT = Calm winds

    Wind direction is reported as true north (not magnetic) and represents
    where the wind is coming FROM (not going to).

    Args:
        obs (Metar): Parsed METAR observation object

    Returns:
        str: Human-readable wind description
    """
    if not obs.wind_speed:
        return "Wind: Calm"

    # Extract wind speed in both knots (aviation standard) and mph (common usage)
    speed_kts = obs.wind_speed.value("KT")
    speed_mph = obs.wind_speed.value("MPH")

    # Calm winds (less than 1 knot)
    if speed_kts < 1:
        return "Wind: Calm"

    # Determine wind direction
    # VRB (variable) is used when direction varies by 60° or more
    direction = "variable"
    if obs.wind_dir:
        degrees = obs.wind_dir.value()
        # Convert degrees to compass direction (e.g., 310° = northwest)
        direction = degrees_to_direction(degrees)

    wind_text = f"Wind: {speed_mph:.0f} mph ({speed_kts:.0f} knots) from the {direction}"

    # Add gust information if present
    # Gusts are reported when wind speed varies by 10+ knots
    if obs.wind_gust:
        gust_kts = obs.wind_gust.value("KT")
        gust_mph = obs.wind_gust.value("MPH")
        wind_text += f", gusting to {gust_mph:.0f} mph ({gust_kts:.0f} knots)"

    return wind_text


def degrees_to_direction(degrees):
    """
    Convert wind direction from degrees to cardinal direction name.

    The compass is divided into 16 equal sectors of 22.5° each.
    Wind direction in METAR is reported in 10° increments rounded to
    the nearest 10° (e.g., 310°, 320°, 330°).

    Direction Mapping:
        0° (360°) = North
        90° = East
        180° = South
        270° = West
        45° = Northeast, etc.

    Args:
        degrees (float): Wind direction in degrees (0-360)

    Returns:
        str: Cardinal direction name (e.g., "north", "northwest", "south-southeast")

    Example:
        >>> degrees_to_direction(310)
        'northwest'
        >>> degrees_to_direction(45)
        'northeast'
    """
    # 16-point compass rose (cardinal and intercardinal directions)
    directions = ['north', 'north-northeast', 'northeast', 'east-northeast',
                 'east', 'east-southeast', 'southeast', 'south-southeast',
                 'south', 'south-southwest', 'southwest', 'west-southwest',
                 'west', 'west-northwest', 'northwest', 'north-northwest']

    # Calculate index: Add 11.25° offset for proper rounding, divide by sector size
    # Modulo 16 wraps around (360° back to north)
    index = int((degrees + 11.25) / 22.5) % 16
    return directions[index]


def get_weather_phenomena(obs):
    """
    Decode present weather phenomena (precipitation, obscuration, etc.).

    METAR Weather Codes:
        Intensity:
            - = Light
            (no prefix) = Moderate
            + = Heavy

        Descriptors:
            MI = Shallow    BC = Patches    DR = Drifting
            BL = Blowing    SH = Showers    TS = Thunderstorm
            FZ = Freezing   PR = Partial

        Phenomena:
            RA = Rain       SN = Snow       DZ = Drizzle
            FG = Fog        BR = Mist       HZ = Haze
            GR = Hail       GS = Small hail
            SQ = Squalls    FC = Funnel cloud

    Examples:
        -RA = Light rain
        +TSRA = Heavy thunderstorms with rain
        FZFG = Freezing fog

    Args:
        obs (Metar): Parsed METAR observation object

    Returns:
        str: Human-readable weather phenomena description or None
    """
    if not obs.weather:
        return None

    phenomena = []
    # Each weather item is a tuple: (code, description, human_readable)
    for wx in obs.weather:
        phenomena.append(wx[2])  # Index 2 contains human-readable description

    return "Weather: " + ", ".join(phenomena) if phenomena else None


def create_summary(obs):
    """
    Create a concise, friendly one-sentence weather summary.

    This function generates a brief overview suitable for quick reading,
    combining the most important weather elements into a natural sentence.

    Format: "[Sky], [Temperature], [Wind], [Weather phenomena]."
    Example: "Clear skies, 72°F, winds 8 mph from the south."

    Args:
        obs (Metar): Parsed METAR observation object

    Returns:
        str: One-sentence weather summary ending with a period
    """
    parts = []

    # Simplified sky condition for summary
    # Check all cloud layers to determine overall condition
    if not obs.sky or any(sky[0] in ['CLR', 'SKC'] for sky in obs.sky):
        parts.append("Clear skies")
    elif any(sky[0] == 'OVC' for sky in obs.sky):
        parts.append("Overcast")  # Complete cloud coverage
    elif any(sky[0] in ['BKN', 'SCT'] for sky in obs.sky):
        parts.append("Partly cloudy")  # Scattered or broken clouds
    else:
        parts.append("Few clouds")  # Minimal cloud coverage

    # Temperature in Fahrenheit (more common for general users)
    if obs.temp:
        temp_f = (obs.temp.value() * 9/5) + 32
        parts.append(f"{temp_f:.0f}°F")

    # Wind information (simplified for summary)
    if obs.wind_speed:
        speed_mph = obs.wind_speed.value("MPH")
        if speed_mph < 1:
            parts.append("calm winds")
        else:
            direction = "variable direction"
            if obs.wind_dir:
                degrees = obs.wind_dir.value()
                direction = f"from the {degrees_to_direction(degrees)}"
            parts.append(f"winds {speed_mph:.0f} mph {direction}")
    else:
        parts.append("calm winds")

    # Include any significant weather phenomena (rain, snow, etc.)
    if obs.weather:
        # Convert to lowercase for better sentence flow
        weather_desc = ", ".join([wx[2].lower() for wx in obs.weather])
        parts.append(weather_desc)

    # Join all parts with commas and add period
    return ", ".join(parts) + "."
