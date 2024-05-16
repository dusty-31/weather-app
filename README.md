
---

# Weather App

A Python-based command-line application to fetch and display weather information for a city using the OpenWeatherMap API. The application allows users to choose between viewing the current weather and a 5-day forecast.

## Features

- Fetch current weather data for a specified city.
- Fetch 5-day weather forecast data for a specified city.
- Display weather information in both metric and imperial units.
- Interactive menu for selecting the type of weather information to display.

## Requirements

- Python 3.6 or higher
- OpenWeatherMap API key

## Installation

1. Clone the repository or download the script.

2. Install the required Python packages using pip:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `settings.ini` file in the same directory as the script and add your OpenWeatherMap API key:

    ```ini
    [openweather]
    api_key = your_api_key_here
    ```

## Usage

Run the script from the command line with the required arguments.

### Command-Line Arguments

- `city` (required): The name of the city for which you want to fetch the weather data.
- `-i`, `--imperial` (optional): Display the temperature in imperial units (Fahrenheit).

### Example

To get the current weather for London in metric units:

```sh
python app.py London
```

To get the current weather for New York in imperial units:

```sh
python app.py New York -i
```

### Interactive Menu

After running the script, you will be presented with a menu to choose between viewing the current weather or the 5-day forecast:

```
Choose an option:
1. Current Weather
2. 5-Day Forecast
3. Exit
Enter your choice (1/2/3):
```

Enter `1` to view the current weather, `2` to view the 5-day forecast, or `3` to exit the program.

## Functions

### `get_api_key()`

Reads the API key from the `settings.ini` file.

### `read_user_cli_args()`

Parses command-line arguments.

### `build_weather_query(base_url, city_input, imperial=False)`

Builds the query URL for the OpenWeatherMap API.

### `get_weather_data(query_url)`

Fetches weather data from the OpenWeatherMap API.

### `display_current_weather_data(data, imperial=False)`

Displays the current weather data.

### `display_forecast_data(forecast_data, imperial=False)`

Displays the 5-day weather forecast data.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Make sure to replace `your_api_key_here` with your actual OpenWeatherMap API key when running the script.