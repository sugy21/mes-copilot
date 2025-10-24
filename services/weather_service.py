from typing import Dict, Any, Optional
from datetime import date
import httpx
from fastapi import HTTPException


async def get_weather_forecast(city: str, forecast_date: date) -> Dict[str, Any]:
    """
    Get weather forecast for a specific city and date using Open-Meteo API

    Args:
        city: City name
        forecast_date: Date to get forecast for

    Returns:
        Dict containing weather data
    """
    # Geocoding data for common cities (in production, use a geocoding API)
    CITY_COORDINATES = {
        "seoul": {"lat": 37.5665, "lon": 126.9780},
        "busan": {"lat": 35.1796, "lon": 129.0756},
        "incheon": {"lat": 37.4563, "lon": 126.7052},
        "daegu": {"lat": 35.8714, "lon": 128.6014},
        "daejeon": {"lat": 36.3504, "lon": 127.3845},
    }

    city = city.lower()
    if city not in CITY_COORDINATES:
        raise HTTPException(status_code=404, detail=f"City '{city}' not supported")

    coords = CITY_COORDINATES[city]

    # Format API URL with parameters
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
        ],
        "timezone": "Asia/Seoul",
        "start_date": forecast_date.isoformat(),
        "end_date": forecast_date.isoformat(),
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Extract relevant data
            daily = data.get("daily", {})

            return {
                "city": city,
                "date": forecast_date.isoformat(),
                "max_temp": daily.get("temperature_2m_max", [None])[0],
                "min_temp": daily.get("temperature_2m_min", [None])[0],
                "precipitation_prob": daily.get(
                    "precipitation_probability_max", [None]
                )[0],
            }

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code, detail=f"Weather API error: {str(e)}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Could not connect to weather service: {str(e)}"
        )
