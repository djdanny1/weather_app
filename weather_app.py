import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env in the project root
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str, units: str = "metric"):
    if not API_KEY:
        print("[!] Missing API key. Set OPENWEATHER_API_KEY in your .env file.")
        return None

    params = {"q": city, "appid": API_KEY, "units": units}
    try:
        r = requests.get(BASE_URL, params=params, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Network/API error: {e}")
        return None

    data = r.json()
    if data.get("cod") != 200:
        print(f"[!] API error: {data.get('message')}")
        return None

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"].title(),
        "units": "°C" if units == "metric" else "°F",
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python weather_app.py <city> [--imperial]")
        sys.exit(1)

    city_parts = []
    units = "metric"
    for arg in sys.argv[1:]:
        if arg == "--imperial":
            units = "imperial"
        else:
            city_parts.append(arg)

    city = " ".join(city_parts)
    weather = get_weather(city, units=units)
    if not weather:
        sys.exit(1)

    print(f"\nWeather in {weather['city']}:")
    print(f"Temperature: {weather['temp']}{weather['units']}")
    print(f"Humidity: {weather['humidity']}%")
    print(f"Condition: {weather['condition']}\n")

if __name__ == "__main__":
    main()
