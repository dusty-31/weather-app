import argparse
from configparser import ConfigParser
from urllib import parse, request, error
import json
import ssl
import certifi
from datetime import datetime, timezone

CURRENT_WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'


def get_api_key():
    config = ConfigParser()
    config.read('settings.ini')
    try:
        api_key = config['openweather']['api_key']
    except KeyError:
        raise KeyError('API key not found in the configuration file.')
    return api_key


def read_user_cli_args():
    parser = argparse.ArgumentParser(
        description='gets weather and temperature information for a city'
    )
    parser.add_argument(
        'city', nargs='+', type=str, help='enter the city name'
    )
    parser.add_argument(
        '-i',
        '--imperial',
        action='store_true',
        help='display the temperature in imperial units',
    )
    return parser.parse_args()


def build_weather_query(base_url, city_input, imperial=False):
    api_key = get_api_key()
    # print(f'Using API key: {api_key}')  # Debugging line
    city_name = ' '.join(city_input)
    url_encoded_city_name = parse.quote_plus(city_name)
    units = 'imperial' if imperial else 'metric'
    url = (
        f'{base_url}?q={url_encoded_city_name}'
        f'&units={units}&appid={api_key}'
    )
    return url


def get_weather_data(query_url):
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        response = request.urlopen(query_url, context=context)
        data = response.read()
        return json.loads(data)
    except error.HTTPError as e:
        if e.code == 401:
            print('HTTP Error 401: Check your API key.')
        elif e.code == 404:
            print('HTTP Error 404: City not found.')
        print(f'HTTP Error: {e.code} - {e.reason}')
    except error.URLError as e:
        print(f'URL Error: {e.reason}')
    except json.JSONDecodeError as e:
        print(f'JSON Decode Error: {e.msg}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


def display_current_weather_data(data, imperial=False):
    city = data.get('name', 'N/A')
    weather = data.get('weather', [{}])[0]
    weather_description = weather.get('description', 'N/A')
    main = data.get('main', {})
    temperature = main.get('temp', 'N/A')
    feels_like = main.get('feels_like', 'N/A')
    temp_min = main.get('temp_min', 'N/A')
    temp_max = main.get('temp_max', 'N/A')
    pressure = main.get('pressure', 'N/A')
    humidity = main.get('humidity', 'N/A')
    wind = data.get('wind', {})
    wind_speed = wind.get('speed', 'N/A')
    wind_deg = wind.get('deg', 'N/A')
    clouds = data.get('clouds', {}).get('all', 'N/A')
    visibility = data.get('visibility', 'N/A')
    sys = data.get('sys', {})
    country = sys.get('country', 'N/A')

    unit = 'F' if imperial else 'C'
    wind_speed_unit = 'mph' if imperial else 'm/s'

    print(f'{'City:':<20} {city}, {country}')
    print(f'{'Weather:':<20} {weather_description.capitalize()}')
    print(f'{'Temperature:':<20} {temperature}°{unit}')
    print(f'{'Feels Like:':<20} {feels_like}°{unit}')
    print(f'{'Min Temperature:':<20} {temp_min}°{unit}')
    print(f'{'Max Temperature:':<20} {temp_max}°{unit}')
    print(f'{'Pressure:':<20} {pressure} hPa')
    print(f'{'Humidity:':<20} {humidity}%')
    print(f'{'Wind Speed:':<20} {wind_speed} {wind_speed_unit}')
    print(f'{'Wind Direction:':<20} {wind_deg}°')
    print(f'{'Cloudiness:':<20} {clouds}%')
    print(f'{'Visibility:':<20} {visibility} m')


def display_forecast_data(forecast_data, imperial=False):
    city = forecast_data.get("city", {}).get("name", "N/A")
    country = forecast_data.get("city", {}).get("country", "N/A")
    forecast_list = forecast_data.get("list", [])

    unit = 'F' if imperial else 'C'
    wind_speed_unit = 'mph' if imperial else 'm/s'

    print(f"5-Day Weather Forecast for {city}, {country}\n")

    current_date = ""
    for forecast in forecast_list:
        dt = forecast.get("dt", 0)
        date_time = datetime.fromtimestamp(dt, tz=timezone.utc)
        date_str = date_time.strftime('%Y-%m-%d')
        time_str = date_time.strftime('%H:%M:%S')

        if current_date != date_str:
            current_date = date_str
            print(f"\nDate: {current_date}")
            print("-" * 40)

        temp = forecast.get("main", {}).get("temp", "N/A")
        feels_like = forecast.get("main", {}).get("feels_like", "N/A")
        weather_description = forecast.get("weather", [{}])[0].get("description", "N/A")
        wind_speed = forecast.get("wind", {}).get("speed", "N/A")

        print(f"Time: {time_str} UTC")
        print(f"  Temperature: {temp}°{unit}")
        print(f"  Feels Like: {feels_like}°{unit}")
        print(f"  Weather: {weather_description.capitalize()}")
        print(f"  Wind Speed: {wind_speed} {wind_speed_unit}")
        print("-" * 40)


def main():
    user_args = read_user_cli_args()

    while True:
        print("\nChoose an option:")
        print("1. Current Weather")
        print("2. 5-Day Forecast")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            query_url = build_weather_query(CURRENT_WEATHER_URL, user_args.city, user_args.imperial)
            print(f'Query URL: {query_url}')
            try:
                weather_data = get_weather_data(query_url)
                if weather_data:
                    display_current_weather_data(weather_data, user_args.imperial)
                else:
                    print("No weather data found.")
            except request.HTTPError as e:
                print(f'HTTP error occurred: {e.code} - {e.reason}')
                if e.code == 401:
                    print('Check if your API key is correct and has the necessary permissions.')
        elif choice == '2':
            query_url = build_weather_query(FORECAST_URL, user_args.city, user_args.imperial)
            print(f'Query URL: {query_url}')
            try:
                forecast_data = get_weather_data(query_url)
                if forecast_data:
                    display_forecast_data(forecast_data, user_args.imperial)
                else:
                    print("No weather data found.")
            except request.HTTPError as e:
                print(f'HTTP error occurred: {e.code} - {e.reason}')
                if e.code == 401:
                    print('Check if your API key is correct and has the necessary permissions.')
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == '__main__':
    main()
