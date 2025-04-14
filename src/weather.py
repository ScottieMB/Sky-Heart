import requests
from datetime import datetime, timedelta
import os
import random
import messages

# Weather API
API_KEY = os.getenv('WEATHER_API_KEY')
city = os.getenv('WEATHER_CITY')

# Function to get the weather and local time using JSON data
def get_weather(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_condition = data['weather'][0]['main']  # condition fetcher
        weather_temperature = data['main']['temp'] # temp fetcher
        weather_icon = data['weather'][0]['icon'] # icon fetcher

        weather_icon_url = f"http://openweathermap.org/img/wn/{weather_icon}.png"
        
        # Get timezone and current time
        timezone_offset = data['timezone']
        utc_now = datetime.utcnow()
        local_time = utc_now + timedelta(seconds=timezone_offset)

        return weather_condition, local_time, weather_temperature, weather_icon_url
    else:
        print(f"Error fetching weather data: {data['message']}")
        return None, None
    
# Function to return messages based on the temperature
def weather_messages(weather_temperature):
    if weather_temperature > 32.22:
        return random.choice(messages.hot_messages)
    elif weather_temperature < 32.22 and weather_temperature >= 25.56:
        return random.choice(messages.warm_messages)
    elif weather_temperature < 25.56 and weather_temperature >= 18.33:
        return random.choice(messages.nice_messages)
    elif weather_temperature < 18.33 and weather_temperature >= 7.22:
        return random.choice(messages.cold_messages)
    else:
        return random.choice(messages.freezing_messages)