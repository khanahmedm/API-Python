import requests
from api_key import get_api_key 

# API Details
api_key = get_api_key()
base_url = "https://api.openweathermap.org/data/2.5/weather"

# Parameters
city = "London"
params = {
    "q": city,
    "appid": api_key,
    "units": "metric"  # Use 'imperial' for Fahrenheit
}

# Make the GET request
try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse JSON response
    weather_data = response.json()

    # Extract specific details
    city_name = weather_data["name"]
    temp = weather_data["main"]["temp"]
    weather_description = weather_data["weather"][0]["description"]

    print(f"City: {city_name}")
    print(f"Temperature: {temp}°C")
    print(f"Weather: {weather_description}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
