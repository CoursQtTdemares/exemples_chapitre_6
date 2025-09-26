import secrets
import time
from typing import TypedDict


class WeatherResponse(TypedDict):
    city: str
    temperature: float
    humidity: float


def fetch_weather_data(city: str) -> WeatherResponse:
    time.sleep(3)

    if secrets.randbelow(10) == 0:
        raise TimeoutError("API is not responding")

    return {
        "city": city,
        "temperature": (secrets.randbelow(150) + 100) / 10,  # nombre entre 15 et 25
        "humidity": secrets.randbelow(101),  # nombre entre 0 et 100
    }
