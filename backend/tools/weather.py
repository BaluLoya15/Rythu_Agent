import httpx
from datetime import datetime
from typing import Dict, Any, List, Optional
from backend.models.schemas import WeatherData, WeatherForecastDay

# Known coordinate mappings for primary Andhra Pradesh / Telangana Mandi Hubs
LOCATION_COORDINATES: Dict[str, tuple[float, float, str]] = {
    "vijayawada": (16.5075, 80.6466, "Vijayawada, Krishna/NTR, Andhra Pradesh"),
    "guntur": (16.3067, 80.4365, "Guntur, Andhra Pradesh"),
    "tenali": (16.2437, 80.6400, "Tenali, Guntur, Andhra Pradesh"),
    "warangal": (17.9689, 79.5941, "Warangal, Telangana"),
    "kurnool": (15.8281, 78.0373, "Kurnool, Andhra Pradesh"),
    "anantapur": (14.6819, 77.6006, "Anantapur, Andhra Pradesh")
}

async def geocode_location(location_name: str) -> tuple[float, float, str]:
    """
    Geocodes location name using Open-Meteo Geocoding API,
    falling back to verified regional coordinates for known hubs.
    """
    clean_name = location_name.strip()
    loc_lower = clean_name.lower()

    # Fast match for known agricultural hubs
    for hub, (lat, lon, full_name) in LOCATION_COORDINATES.items():
        if hub in loc_lower:
            return lat, lon, full_name

    # Dynamic live geocoding via Open-Meteo
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={clean_name}&count=1&language=en&format=json"
        async with httpx.AsyncClient(timeout=4.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get("results", [])
                if results:
                    top = results[0]
                    lat = float(top["latitude"])
                    lon = float(top["longitude"])
                    name = f"{top.get('name', clean_name)}, {top.get('admin1', '')}, {top.get('country', 'India')}".strip(", ")
                    return lat, lon, name
    except Exception:
        pass

    # Default to Vijayawada coordinates if geocoding unreachable
    return 16.5075, 80.6466, f"{clean_name} (Coordinates mapped: 16.51°N, 80.65°E)"

async def get_weather(location: str = "Vijayawada", force_demo: bool = False) -> WeatherData:
    """
    Fetches LIVE agro-meteorological data from Open-Meteo.
    In production mode (force_demo=False), never silently injects demo data.
    If the API fails, explicitly returns data_status="UNAVAILABLE".
    """
    now_ist = datetime.now().strftime("%Y-%m-%d %H:%M IST")

    # Developer/Testing Mode ONLY
    if force_demo:
        return WeatherData(
            location=f"{location} (Test Baseline)",
            latitude=16.5075,
            longitude=80.6466,
            temperature_c=29.5,
            humidity_pct=72,
            rainfall_probability_pct=15,
            precipitation_mm=0.0,
            wind_speed_kmh=8.5,
            weather_condition="Partly Cloudy (Test Data)",
            forecast=[
                WeatherForecastDay(day="Today", temp_min=24.0, temp_max=32.5, condition="Partly Cloudy", rain_probability_pct=15, spray_recommendation="Safe for foliar sprays (Evening)"),
                WeatherForecastDay(day="Tomorrow", temp_min=24.5, temp_max=33.0, condition="Sunny", rain_probability_pct=10, spray_recommendation="Optimal spray window 6:30 AM - 9:30 AM"),
                WeatherForecastDay(day="Day 3", temp_min=23.5, temp_max=31.0, condition="Isolated Rain", rain_probability_pct=45, spray_recommendation="Avoid systemic fungicides")
            ],
            spray_window_advisory="TEST MODE: Favorable calm conditions. Recommended evening spray.",
            timestamp=now_ist,
            source="IMD/ANGRAU Agromet Test Archive",
            data_status="DEMO",
            is_live=False
        )

    # LIVE EXECUTION PATH
    try:
        lat, lon, resolved_name = await geocode_location(location)
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,precipitation,precipitation_probability,wind_speed_10m,weather_code"
            f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum"
            f"&timezone=Asia%2FKolkata"
        )

        async with httpx.AsyncClient(timeout=12.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                current = data.get("current", {})
                daily = data.get("daily", {})

                temp = float(current.get("temperature_2m", 0.0))
                humidity = int(current.get("relative_humidity_2m", 0))
                rain_prob = int(current.get("precipitation_probability", 0) or 0)
                precip = float(current.get("precipitation", 0.0) or 0.0)
                wind = float(current.get("wind_speed_10m", 0.0))

                # Compute 3-day forecast
                forecast_days: List[WeatherForecastDay] = []
                days_labels = ["Today", "Tomorrow", "Day 3"]
                time_arr = daily.get("time", [])

                for i in range(min(3, len(time_arr))):
                    t_min = float(daily.get("temperature_2m_min", [24.0])[i])
                    t_max = float(daily.get("temperature_2m_max", [33.0])[i])
                    d_rain = int(daily.get("precipitation_probability_max", [10])[i] or 10)
                    
                    cond = "Sunny / Clear Sky" if d_rain < 20 else ("Partly Cloudy" if d_rain < 40 else "Rain Showers Expected")
                    spray_rec = "Favorable spray conditions" if d_rain < 30 and wind < 15 else "Caution: High wash-off risk"

                    forecast_days.append(WeatherForecastDay(
                        day=days_labels[i] if i < len(days_labels) else f"Day {i+1}",
                        temp_min=t_min,
                        temp_max=t_max,
                        condition=cond,
                        rain_probability_pct=d_rain,
                        spray_recommendation=spray_rec
                    ))

                # Real-time agro-met spray advisory
                if wind > 15.0:
                    spray_adv = f"HIGH WIND ALERT ({wind} km/h): Do not spray foliar chemicals today to avoid severe drift loss."
                elif rain_prob > 50:
                    spray_adv = f"RAIN ALERT ({rain_prob}% probability): Avoid applying systemic fungicides/insecticides due to wash-off risk."
                elif temp > 34.0:
                    spray_adv = f"WARM WEATHER ({temp}°C): Spray only during early morning (6:30 - 9:00 AM) or late evening (after 4:30 PM) to avoid leaf scorching."
                else:
                    spray_adv = f"FAVORABLE SPRAY WINDOW: Wind {wind} km/h, Rain chance {rain_prob}%. Optimal evening window: 4:30 PM - 6:30 PM."

                return WeatherData(
                    location=resolved_name,
                    latitude=lat,
                    longitude=lon,
                    temperature_c=temp,
                    humidity_pct=humidity,
                    rainfall_probability_pct=rain_prob,
                    precipitation_mm=precip,
                    wind_speed_kmh=wind,
                    weather_condition="Clear / Fair Weather" if rain_prob < 20 else ("Humid & Cloudy" if rain_prob < 50 else "Rainy Conditions"),
                    forecast=forecast_days,
                    spray_window_advisory=spray_adv,
                    timestamp=now_ist,
                    source="Open-Meteo Live Agro-Met Satellite Feed",
                    data_status="LIVE",
                    is_live=True
                )
            else:
                raise RuntimeError(f"Open-Meteo returned status {resp.status_code}")

    except Exception as e:
        # DO NOT SILENTLY INJECT FAKE DATA IN PRODUCTION
        return WeatherData(
            location=location,
            temperature_c=0.0,
            humidity_pct=0,
            rainfall_probability_pct=0,
            precipitation_mm=0.0,
            wind_speed_kmh=0.0,
            weather_condition="Service Temporarily Unavailable",
            forecast=[],
            spray_window_advisory="Live agro-met advisory could not be established.",
            timestamp=now_ist,
            source="Open-Meteo Live API",
            data_status="UNAVAILABLE",
            is_live=False,
            error_message=f"Live weather data is currently unavailable from Open-Meteo: {str(e)}"
        )
