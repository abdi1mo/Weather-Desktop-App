"""
Mohamed Abdi
COMP492 Project
Weather App Desktop
This app uses OpenWeatherApp API to gather current weather info.
"""
# Importing necessary modules
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Function to get the current weather using OpenWeatherMap API
def get_current_weather(api_key, location, units):
    """
    Retrieves the current weather information from the OpenWeatherMap API.

    Parameters:
    - api_key (str): OpenWeatherMap API key
    - location (str): City name or Zip Code
    - units (str): Measurement units ('metric' or 'imperial')

    Returns:
    - dict: JSON response containing weather data
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            return None
    except requests.ConnectionError:
        messagebox.showerror("Error", "Check your internet connection")
        return None

# Function to get the 7-day forecast using OpenWeatherMap API
def get_7_day_forecast(api_key, location, units):
    """
    Retrieves the 7-day weather forecast from the OpenWeatherMap API.

    Parameters:
    - api_key (str): OpenWeatherMap API key
    - location (str): City name or Zip Code
    - units (str): Measurement units ('metric' or 'imperial')

    Returns:
    - dict: JSON response containing forecast data
    """
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            return None
    except requests.ConnectionError:
        messagebox.showerror("Error", "Check your internet connection")
        return None

# Function to get the 24-hour forecast using OpenWeatherMap API
def get_24_hour_forecast(api_key, location, units):
    """
    Retrieves the 24-hour weather forecast from the OpenWeatherMap API.

    Parameters:
    - api_key (str): OpenWeatherMap API key
    - location (str): City name or Zip Code
    - units (str): Measurement units ('metric' or 'imperial')

    Returns:
    - dict: JSON response containing forecast data
    """
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            return None
    except requests.ConnectionError:
        messagebox.showerror("Error", "Check your internet connection")
        return None

# Function to display the current weather information in the GUI
def display_current_weather(weather_data, units):
    """
    Displays the current weather information in the GUI.

    Parameters:
    - weather_data (dict): JSON response containing weather data
    - units (str): Measurement units ('metric' or 'imperial')
    """
    if weather_data:
        description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        if units == 'metric':
            unit_label = "°C"
            speed_unit = "m/s"
        else:
            unit_label = "°F"
            speed_unit = "mph"

        result_text = (
            f"Description: {description}\n\n"
            f"Temperature: {temperature}{unit_label}\n\n"
            f"Humidity: {humidity}%\n\n"
            f"Wind Speed: {wind_speed} {speed_unit}"
        )
        result_label.config(text=result_text)
    else:
        messagebox.showerror("Error", "Location not found")

# Function to display the 7-day forecast information in the GUI
def display_7_day_forecast(forecast_data, units):
    """
    Displays the 7-day forecast information in the GUI.

    Parameters:
    - forecast_data (dict): JSON response containing forecast data
    - units (str): Measurement units ('metric' or 'imperial')
    """
    if forecast_data:
        daily_forecasts = {}
        for entry in forecast_data['list']:
            date = entry['dt_txt'].split()[0]
            formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %d, %Y')

            if formatted_date not in daily_forecasts:
                daily_forecasts[formatted_date] = {
                    'temperature': entry['main']['temp'],
                    'description': entry['weather'][0]['description'],
                    'wind_speed': entry['wind']['speed'],
                    'precipitation': entry['rain']['3h'] if 'rain' in entry else 0
                }

        if units == 'metric':
            unit_label_temp = "°C"
            unit_label_speed = "m/s"
            unit_label_precip = "mm"
        else:
            unit_label_temp = "°F"
            unit_label_speed = "mph"
            unit_label_precip = "in"

        forecast_text = "7-Day Forecast:\n\n"

        for date, data in daily_forecasts.items():
            forecast_text += (
                f"{date}:\n"
                f"  - Description: {data['description']}\n"
                f"  - Temperature: {data['temperature']}{unit_label_temp}\n"
                f"  - Wind: {data['wind_speed']} {unit_label_speed}\n"
                f"  - Precipitation: {data['precipitation']} {unit_label_precip}\n\n"
            )

        result_label.config(text=forecast_text)
    else:
        messagebox.showerror("Error", "Location not found")

# Function to display the 24-hour forecast information in the GUI
def display_24_hour_forecast(forecast_data, units):
    """
    Displays the 24-hour forecast information in the GUI.

    Parameters:
    - forecast_data (dict): JSON response containing forecast data
    - units (str): Measurement units ('metric' or 'imperial')
    """
    if forecast_data:
        hourly_forecasts = forecast_data['list'][:24]

        if units == 'metric':
            unit_label_temp = "°C"
            unit_label_speed = "m/s"
            unit_label_precip = "mm"
        else:
            unit_label_temp = "°F"
            unit_label_speed = "mph"
            unit_label_precip = "in"

        # Clear previous content in result_label
        result_label.config(text="")

        # Create a Treeview
        tree = ttk.Treeview(result_label, columns=("Date", "Time", "Description", "Temperature", "Wind Speed", "Precipitation"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Description", text="Description")
        tree.heading("Temperature", text="Temperature")
        tree.heading("Wind Speed", text="Wind Speed")
        tree.heading("Precipitation", text="Precipitation")

        # Insert data into the Treeview
        for hour in hourly_forecasts:
            date, time = hour['dt_txt'].split()
            time = datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')
            temperature = f"{hour['main']['temp']}{unit_label_temp}"
            description = hour['weather'][0]['description']
            wind_speed = f"{hour['wind']['speed']} {unit_label_speed}"
            precipitation = f"{hour['rain']['3h'] if 'rain' in hour else 0} {unit_label_precip}"

            tree.insert("", "end", values=(date, time, description, temperature, wind_speed, precipitation))

        tree.grid(row=3, column=0, columnspan=3, pady=10)
    else:
        messagebox.showerror("Error", "Location not found")

# Function to fetch and display the current weather when the button is clicked
def fetch_current_weather():
    location = location_entry.get()
    units = units_var.get()
    api_key = '56d8124f9b28d206da6342c56e9f6453'

    if not api_key:
        messagebox.showerror("Error", "Please enter your OpenWeatherMap API key")
        return

    weather_data = get_current_weather(api_key, location, units)
    display_current_weather(weather_data, units)

# Function to fetch and display the 7-day forecast when the button is clicked
def fetch_7_day_forecast():
    location = location_entry.get()
    units = units_var.get()
    api_key = '56d8124f9b28d206da6342c56e9f6453'

    if not api_key:
        messagebox.showerror("Error", "Please enter your OpenWeatherMap API key")
        return

    forecast_data = get_7_day_forecast(api_key, location, units)
    display_7_day_forecast(forecast_data, units)

# Function to fetch and display the 24-hour forecast when the button is clicked
def fetch_24_hour_forecast():
    location = location_entry.get()
    units = units_var.get()
    api_key = '56d8124f9b28d206da6342c56e9f6453'

    if not api_key:
        messagebox.showerror("Error", "Please enter your OpenWeatherMap API key")
        return

    forecast_data = get_24_hour_forecast(api_key, location, units)
    display_24_hour_forecast(forecast_data, units)

# GUI setup
app = tk.Tk()
app.title("Weather App")

# Widgets
location_label = tk.Label(app, text="Enter City or Zip Code:")
location_label.grid(row=0, column=0, padx=10, pady=10)

location_entry = tk.Entry(app)
location_entry.grid(row=0, column=1, padx=10, pady=10)

units_var = tk.StringVar(value='metric')  # Default to metric units

units_label = tk.Label(app, text="Units:")
units_label.grid(row=1, column=0, pady=10)

metric_radio = tk.Radiobutton(app, text="Metric", variable=units_var, value='metric')
metric_radio.grid(row=1, column=1, pady=10)

imperial_radio = tk.Radiobutton(app, text="Imperial", variable=units_var, value='imperial')
imperial_radio.grid(row=1, column=2, pady=10)

current_weather_button = tk.Button(app, text="Current Weather", command=fetch_current_weather)
current_weather_button.grid(row=2, column=0, pady=10)

forecast_7_day_button = tk.Button(app, text="7-Day Forecast", command=fetch_7_day_forecast)
forecast_7_day_button.grid(row=2, column=1, pady=10)

forecast_24_hour_button = tk.Button(app, text="24-Hour Forecast", command=fetch_24_hour_forecast)
forecast_24_hour_button.grid(row=2, column=2, pady=10)

result_label = tk.Label(app, text="")
result_label.grid(row=3, column=0, columnspan=3, pady=10)

# Main application loop
app.mainloop()

