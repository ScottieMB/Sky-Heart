import os
import requests
import pygame
from datetime import datetime, timedelta
import pytz
import random
import math
import spotipy
import io
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify credentials (OAuth 2.0)
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                       client_secret=client_secret,
                                       redirect_uri="http://localhost:8080/callback",
                                       scope="user-read-playback-state user-modify-playback-state"))

# Weather API
API_KEY = os.getenv('WEATHER_API_KEY')
city = os.getenv('WEATHER_CITY')

# Initialize Pygame
pygame.init()
caption = pygame.display.set_caption.os.getenv('YOUR_CAPTION')

# Window display constants
WIDTH, HEIGHT = 650, 500

# Button settings (Play button)
BUTTON_WIDTH, BUTTON_HEIGHT = 50, 50
button_x = WIDTH - BUTTON_WIDTH - 10
button_y = 10

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Timer settings
target_date = os.getenv('YOUR_DATETIME')

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the font using an absolute path
font_path = os.path.join(script_dir, 'assets/Grand9kPixel.ttf')
font = pygame.font.Font(font_path, 15)

# Hardcoded list of songs (format - spotify:track:(spotify ID))
songs = [
    "<your-tracks-here>"
]

# Messages
morning_messages = [
    "Goodmorning!"
]

latemorning_messages = [
    "Goodmorning (still)!"
]

afternoon_messages = [
    "Good afternoon!"
]

evening_messages = [
    "Good evening!"
]

night_messages = [
    "Goodnight!"
]

hot_messages = [
    "Hot message"
]

warm_messages = [
    "Warm message"
]

nice_messages = [
    "Nice message"
]

cold_messages = [
    "Cold message"
]

freezing_messages = [
    "Freezing message"
]

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

# Function to load the weather icon in the input city
def load_weather_icon(url):
    response = requests.get(url)
    image_data = io.BytesIO(response.content)
    image = pygame.image.load(image_data)
    return image

# Function to determine if it's night time (adjust the hours to your perception of night time)
def is_night_time(local_time):
    return local_time.hour >= 19 or local_time.hour < 5

# Function to load images based on the weather parameters
def load_images(weather_condition, weather_temperature, night_time, weather_icon_url):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load background images based on the weather condition
    if night_time:
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/nighttime.jpg'))  # Load nighttime image
    elif weather_condition == "Clear":
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/sun.png.jpg'))
    elif weather_condition == "Rain":
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/rain.png'))
    elif weather_condition == "Snow":
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/snow.png.jpg'))
    elif weather_condition == "Clouds":
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/cloudy.jpg'))
    else:
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/sun.png.jpg'))

    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale image
    print(f"Current weather condition: {weather_condition}")
    print(f"Current weather condition: {weather_temperature}")
    return background_image, heart_image

# Fuction to return messages based on the local time
def love_messages(local_time):
    if local_time.hour >= 5 and local_time.hour < 8:
        return random.choice(morning_messages)
    elif local_time.hour >= 8 and local_time.hour < 12:
        return random.choice(latemorning_messages)
    elif local_time.hour >= 12 and local_time.hour < 17:
        return random.choice(afternoon_messages)
    elif local_time.hour >= 17 and local_time.hour < 20:
        return random.choice(evening_messages)
    else:
        return random.choice(night_messages)

# Function to return messages based on the temperature
def temp_messages(weather_temperature):
    if weather_temperature > 32.22:
        return random.choice(hot_messages)
    elif weather_temperature < 32.22 and weather_temperature >= 25.56:
        return random.choice(warm_messages)
    elif weather_temperature < 25.56 and weather_temperature >= 18.33:
        return random.choice(nice_messages)
    elif weather_temperature < 18.33 and weather_temperature >= 7.22:
        return random.choice(cold_messages)
    else:
        return random.choice(freezing_messages)

# Function to draw the countdown timer and messages
def draw_timer(screen, current_message, current_temperature):
    remaining_time = target_date - datetime.now()
    days, seconds = remaining_time.days, remaining_time.seconds
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    seconds = seconds % 60

    # Create a formatted string for the timer
    timer_text = f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"
    timer_surface = font.render(timer_text, True, (255, 255, 255))  # Render text

    # Get the width and height of the timer surface
    text_width = timer_surface.get_width()
    text_height = timer_surface.get_height()

    # Calculate the position to center the text
    x_position = (WIDTH - text_width) // 2
    y_position = (HEIGHT - text_height) // 2

    # Draw the timer at the calculated position
    screen.blit(timer_surface, (x_position, y_position))

    # Draw temperature message in the bottom right (parameters are (message, text-smoothing, color))
    message_surface2 = font.render(current_temperature, True, (255, 255, 255))

    # Draw the random message above the timer
    message_surface = font.render(current_message, True, (255, 255, 255))

    # Get the width and height of the message surface
    message_width = message_surface.get_width()
    message_height = message_surface.get_height()
    message2_width = message_surface2.get_width()
    message2_height = message_surface2.get_height()

    # Calculate the position to center the message above the timer
    message_x_position = (WIDTH - message_width) // 2  # Center horizontally
    message_y_position = y_position - message_height - 10  # Position above the timer with some spacing

    # Calculate to be next to the weather icon
    message2_x_position = (WIDTH - message2_width - 12)
    message2_y_position = (HEIGHT - message2_height - 12)

    # Draw the message at the calculated position
    screen.blit(message_surface, (message_x_position, message_y_position))

    screen.blit(message_surface2, (message2_x_position, message2_y_position))

# Function to load the play button
def load_play_button_image():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    play_button_image = pygame.image.load(os.path.join(script_dir, 'assets/play.png')) 
    return pygame.transform.scale(play_button_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

# Function to draw the play button at the top right of the screen
def draw_play_button(screen, play_button_image):
    screen.blit(play_button_image, (button_x, button_y))

# Function to draw the full circle of hearts
def draw_circle_of_hearts(screen, heart_image, num_hearts, radius, angle_offset, spacing_factor=1.5, padding=30):
    center_x, center_y = WIDTH // 2, HEIGHT // 2  # Center of the screen
    adjusted_radius = radius + padding  # Adjusted radius with padding
    angle_between_hearts = (360 / num_hearts) * spacing_factor  # Adjust angle for spacing

    # Load heart image and scale it
    heart_image = pygame.image.load(os.path.join(script_dir, 'assets/heart.png')).convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (50, 50))

    # Main loop to iterate through the number of hearts to put in a circle and rotate
    for i in range(num_hearts):
        # Calculate the angle for heart in radians
        angle = math.radians(i * angle_between_hearts + angle_offset)

        # Calculate x and y position on window based on the angle to get a circular pattern around the center of the screen
        heart_x = int(center_x + adjusted_radius * math.cos(angle) - heart_image.get_width() / 2)
        heart_y = int(center_y + adjusted_radius * math.sin(angle) - heart_image.get_height() / 2)

        # Rotate the heart image
        rotated_heart_image = pygame.transform.rotate(heart_image, -math.degrees(angle))

        # Get the rect of the rotated heart image and set its position to the center of the heart png
        rotated_rect = rotated_heart_image.get_rect(center=(heart_x + heart_image.get_width() / 2, heart_y + heart_image.get_height() / 2))

        # Draw the rotated heart image
        screen.blit(rotated_heart_image, rotated_rect.topleft)

# Function to fetch and play a random song
def play_random_song():
    # Get devices (use this for error checking)
    devices = sp.devices()
    print(devices)
    if not devices['devices']:
        print("No active devices found. Please open the Spotify app on your device and try again.")
        return None, None

    # Choose the first available device
    active_device = devices['devices'][0]
    device_id = active_device['id']

    # Choose a random song
    song_uri = random.choice(songs)
    
    # Extract the track ID from the URI
    track_id = song_uri.split(':')[-1]

    try:
        # Start playback on the selected device
        sp.start_playback(device_id=device_id, uris=[song_uri])

        # Fetch track details
        track_info = sp.track(track_id)
        song_title = track_info['name'] 
        artists = track_info['artists']
        artist_names = ', '.join([artist['name'] for artist in artists])  # Join artist names

        return song_title, artist_names
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error playing song: {e}")
        return None, None

# Function to check if access token is expired. If it is, it'll refresh it. (Mainly in case OAuth doesn't refresh it after an hour)
def refresh_access_token(sp):
    if sp.auth_manager.is_token_expired(sp.auth_manager.get_access_token()):
        sp.auth_manager.refresh_access_token(sp.auth_manager.get_refresh_token())
        print("Access token refreshed.")
    else:
        print("Access token is still valid.")

def main():
    print("Access Token: ", sp.auth_manager.get_access_token())
    refresh_access_token(sp)
    
    current_weather, local_time, weather_temperature, weather_icon_url = get_weather(API_KEY, city)
    weather_temperature = (weather_temperature * 9/5) + 32
    if current_weather and local_time and weather_temperature and weather_icon_url:
        night_time = is_night_time(local_time)
        background_image, heart_image = load_images(current_weather, weather_temperature, night_time, weather_icon_url)

        num_hearts = 12
        radius = 150
        angle_offset = 0
        last_fetch_time = datetime.now()
        current_message = love_messages(local_time)
        current_song_title = None
        current_artist_names = None
        current_temperature = temp_messages(weather_temperature) 

        # Load the play button image
        play_button_image = load_play_button_image()

        if weather_icon_url:
            weather_icon_image = load_weather_icon(weather_icon_url)

        running = True
        while running:
            for event in pygame.event.get():
                print(f"Event: {event}")  # Debug line to see events
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle mouse input for the play button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_x <= mouse_pos[0] <= button_x + BUTTON_WIDTH and button_y <= mouse_pos[1] <= button_y + BUTTON_HEIGHT:
                        print("Play button clicked!")
                        current_song_title, current_artist_names = play_random_song()  # Get both song title and artist names
                        print(f"Current Song: {current_song_title}, Artist(s): {current_artist_names}")  # Debug print
            
            # Check if an hour has passed since the last fetch
            current_time = datetime.now()
            if (current_time - last_fetch_time).total_seconds() >= 3600:
                current_weather, local_time, weather_temperature, weather_icon_url = get_weather(API_KEY, city)
                weather_temperature = (weather_temperature * 9/5) + 32
                if current_weather and local_time and weather_temperature and weather_icon_url:
                    night_time = is_night_time(local_time)
                    background_image, heart_image = load_images(current_weather, weather_temperature, night_time, weather_icon_url)
                    last_fetch_time = current_time
                    current_message = love_messages(local_time)
                    current_temperature = temp_messages(weather_temperature)

            # Draw the background
            screen.blit(background_image, (0, 0))

            # Draw weather icon (hardcoded, adjust based on your desired window size)
            icon_rect = weather_icon_image.get_rect()
            icon_rect.bottomright = (640,  470)
            screen.blit(weather_icon_image, icon_rect)

            # Draw temperature
            temperature_text = f"{weather_temperature:.2f}°F"
            temperature_surface = font.render(temperature_text, True, (255, 255, 255))

            # Position the temperature text and draw (bottom right corner)
            temp_rect = temperature_surface.get_rect()
            temp_rect.bottomright = (590, 458)
            screen.blit(temperature_surface, temp_rect)

            # Call the circle of hearts function
            draw_circle_of_hearts(screen, heart_image, num_hearts, radius, angle_offset)

            # Call the draw timer function
            draw_timer(screen, local_time, current_message, current_temperature)

            # Draw the play button
            draw_play_button(screen, play_button_image)

            # Draw the song title and artist names in the top left corner
            if current_song_title is not None:
                song_title_surface = font.render(current_song_title, True, (255, 255, 255))
                screen.blit(song_title_surface, (10, 10))
            
            if current_artist_names is not None:
                artist_names_surface = font.render(current_artist_names, True, (255, 255, 255))
                screen.blit(artist_names_surface, (10, 30))

            angle_offset += 1
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    else:
        print("Failed to retrieve weather data or local time.")

    pygame.quit()

if __name__ == "__main__":
    main()
