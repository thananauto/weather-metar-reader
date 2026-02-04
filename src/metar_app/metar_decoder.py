from metar.Metar import Metar


def decode_metar(metar_string):
    """
    Decode a METAR string into human-readable format.

    Args:
        metar_string: Raw METAR observation string

    Returns:
        dict: Decoded weather information in human-readable format
    """
    try:
        obs = Metar(metar_string)

        # Build human-readable description
        description_parts = []

        # Sky conditions
        sky_condition = get_sky_condition(obs)
        if sky_condition:
            description_parts.append(sky_condition)

        # Temperature
        if obs.temp:
            temp_c = obs.temp.value()
            temp_f = (temp_c * 9/5) + 32
            description_parts.append(f"Temperature: {temp_f:.0f}°F ({temp_c:.0f}°C)")

        # Dew point
        if obs.dewpt:
            dewpt_c = obs.dewpt.value()
            dewpt_f = (dewpt_c * 9/5) + 32
            description_parts.append(f"Dew point: {dewpt_f:.0f}°F ({dewpt_c:.0f}°C)")

        # Wind
        wind_info = get_wind_info(obs)
        if wind_info:
            description_parts.append(wind_info)

        # Visibility
        if obs.vis:
            vis_miles = obs.vis.value("SM")
            if vis_miles >= 10:
                description_parts.append(f"Visibility: {vis_miles:.0f}+ miles (excellent)")
            else:
                description_parts.append(f"Visibility: {vis_miles:.1f} miles")

        # Pressure
        if obs.press:
            pressure_mb = obs.press.value()
            pressure_inhg = pressure_mb * 0.02953
            description_parts.append(f"Pressure: {pressure_inhg:.2f} inHg ({pressure_mb:.0f} mb)")

        # Weather phenomena (rain, snow, etc.)
        weather = get_weather_phenomena(obs)
        if weather:
            description_parts.append(weather)

        # Create a friendly summary sentence
        summary = create_summary(obs)

        return {
            'summary': summary,
            'details': description_parts,
            'station': obs.station_id,
            'time': obs.time.strftime('%Y-%m-%d %H:%M UTC') if obs.time else 'Unknown'
        }

    except Exception as e:
        raise Exception(f"Failed to parse METAR: {str(e)}")


def get_sky_condition(obs):
    """Get human-readable sky condition."""
    if not obs.sky:
        return "Sky condition: Clear"

    conditions = []
    for sky in obs.sky:
        cover = sky[0]
        height = sky[1].value("FT") if sky[1] else None

        cover_desc = {
            'CLR': 'Clear',
            'SKC': 'Clear',
            'FEW': 'Few clouds',
            'SCT': 'Scattered clouds',
            'BKN': 'Broken clouds',
            'OVC': 'Overcast',
            'VV': 'Vertical visibility'
        }.get(cover, cover)

        if height:
            conditions.append(f"{cover_desc} at {height:.0f} feet")
        else:
            conditions.append(cover_desc)

    return "Sky: " + ", ".join(conditions) if conditions else None


def get_wind_info(obs):
    """Get human-readable wind information."""
    if not obs.wind_speed:
        return "Wind: Calm"

    speed_kts = obs.wind_speed.value("KT")
    speed_mph = obs.wind_speed.value("MPH")

    if speed_kts < 1:
        return "Wind: Calm"

    # Wind direction
    direction = "variable"
    if obs.wind_dir:
        degrees = obs.wind_dir.value()
        direction = degrees_to_direction(degrees)

    wind_text = f"Wind: {speed_mph:.0f} mph ({speed_kts:.0f} knots) from the {direction}"

    # Gusts
    if obs.wind_gust:
        gust_kts = obs.wind_gust.value("KT")
        gust_mph = obs.wind_gust.value("MPH")
        wind_text += f", gusting to {gust_mph:.0f} mph ({gust_kts:.0f} knots)"

    return wind_text


def degrees_to_direction(degrees):
    """Convert wind degrees to cardinal direction."""
    directions = ['north', 'north-northeast', 'northeast', 'east-northeast',
                 'east', 'east-southeast', 'southeast', 'south-southeast',
                 'south', 'south-southwest', 'southwest', 'west-southwest',
                 'west', 'west-northwest', 'northwest', 'north-northwest']

    index = int((degrees + 11.25) / 22.5) % 16
    return directions[index]


def get_weather_phenomena(obs):
    """Get human-readable weather phenomena."""
    if not obs.weather:
        return None

    phenomena = []
    for wx in obs.weather:
        phenomena.append(wx[2])  # Human-readable description

    return "Weather: " + ", ".join(phenomena) if phenomena else None


def create_summary(obs):
    """Create a concise, friendly weather summary."""
    parts = []

    # Sky condition
    if not obs.sky or any(sky[0] in ['CLR', 'SKC'] for sky in obs.sky):
        parts.append("Clear skies")
    elif any(sky[0] == 'OVC' for sky in obs.sky):
        parts.append("Overcast")
    elif any(sky[0] in ['BKN', 'SCT'] for sky in obs.sky):
        parts.append("Partly cloudy")
    else:
        parts.append("Few clouds")

    # Temperature
    if obs.temp:
        temp_f = (obs.temp.value() * 9/5) + 32
        parts.append(f"{temp_f:.0f}°F")

    # Wind
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

    # Weather phenomena
    if obs.weather:
        weather_desc = ", ".join([wx[2].lower() for wx in obs.weather])
        parts.append(weather_desc)

    return ", ".join(parts) + "."
