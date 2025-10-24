from fastapi import APIRouter, HTTPException
from datetime import date
from services.weather_service import get_weather_forecast

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/{city}")
async def get_city_weather(city: str, forecast_date: date = date.today()):
    """Get weather forecast for a specific city and date"""
    return await get_weather_forecast(city, forecast_date)
