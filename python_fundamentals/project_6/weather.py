import argparse
from http.client import HTTPException
import json
from urllib.request import Request, urlopen


def fetch_weather(url, timeout=5):
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        data = json.load(response)

    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object.")

    city = data.get("city")
    temperature = data.get("temperature_c")
    condition = data.get("condition")
    if not isinstance(city, str) or not isinstance(condition, str):
        raise ValueError("Weather data must include a city and a condition.")
    if type(temperature) not in (int, float) or not -273.15 <= temperature <= 100:
        raise ValueError("Weather data must include a valid temperature in Celsius.")

    return city, temperature, condition


def main():
    parser = argparse.ArgumentParser(description="Display weather from a JSON endpoint.")
    parser.add_argument(
        "url",
        nargs="?",
        default="http://127.0.0.1:8000/weather.json",
    )
    args = parser.parse_args()
    try:
        city, temperature, condition = fetch_weather(args.url)
    except (OSError, HTTPException, ValueError) as error:
        parser.exit(1, f"Could not read weather: {error}\n")
    print(f"{city}: {temperature:g} °C, {condition}")


if __name__ == "__main__":
    main()
