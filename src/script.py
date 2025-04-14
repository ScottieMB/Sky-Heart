import pygame
from datetime import datetime, timedelta
import os

# Initialize Pygame
pygame.init()
caption = pygame.display.set_caption.os.getenv('YOUR_CAPTION')

import src.songs as songs
import src.weather as weather
import src.images as images
import src.messages as messages
import src.config as config

# Set up the display
screen = pygame.display.set_mode((config.WIDTH,config.HEIGHT))

def celsius_to_fahrenheit(weather_temperature):
    return (weather_temperature * 9/5) + 32

# Function to determine if it's night time (adjust the hours to your perception of night time)
def is_night_time(local_time):
    return local_time.hour >= 19 or local_time.hour < 5

def main():
    # Weather API
    API_KEY = os.getenv('WEATHER_API_KEY')
    city = os.getenv('WEATHER_CITY')
    
    current_weather, local_time, weather_temperature, weather_icon_url = weather.get_weather(API_KEY, city)
    weather_temperature = (weather_temperature * 9/5) + 32
    if current_weather and local_time and weather_temperature and weather_icon_url:
        night_time = is_night_time(local_time)
        background_image, heart_image, play_button_image = images.load_images(current_weather, weather_temperature, night_time, weather_icon_url)

        num_hearts = 12
        radius = 150
        angle_offset = 0
        last_fetch_time = datetime.now()
        current_message = messages.love_messages(local_time)
        current_song_title = None
        current_artist_names = None
        current_temperature = weather.weather_messages(weather_temperature) 

        if weather_icon_url:
            weather_icon_image = images.load_weather_icon(weather_icon_url)

        running = True
        while running:
            for event in pygame.event.get():
                print(f"Event: {event}")  # Debug line to see events
                if event.type == pygame.QUIT:
                    running = False
                
                # Handle mouse input for the play button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if config.button_x <= mouse_pos[0] <= config.button_x + config.BUTTON_WIDTH and config.button_y <= mouse_pos[1] <= config.button_y + config.BUTTON_HEIGHT:
                        print("Play button clicked!")
                        current_song_title, current_artist_names = songs.play_random_song()  # Get both song title and artist names
                        print(f"Current Song: {current_song_title}, Artist(s): {current_artist_names}")  # Debug print
            
            # Check if an hour has passed since the last fetch
            current_time = datetime.now()
            if (current_time - last_fetch_time).total_seconds() >= 3600:
                current_weather, local_time, weather_temperature, weather_icon_url = weather.get_weather(API_KEY, city)
                weather_temperature = (weather_temperature * 9/5) + 32
                if current_weather and local_time and weather_temperature and weather_icon_url:
                    night_time = is_night_time(local_time)
                    background_image, heart_image, play_button_image = images.load_images(current_weather, weather_temperature, night_time, weather_icon_url)
                    last_fetch_time = current_time
                    current_message = messages.love_messages(local_time)
                    current_temperature = weather.weather_messages(weather_temperature)

            # Draw the background
            screen.blit(background_image, (0, 0))

            # Draw weather icon (hardcoded, adjust based on your desired window size)
            icon_rect = weather_icon_image.get_rect()
            icon_rect.bottomright = (640,  470)
            screen.blit(weather_icon_image, icon_rect)

            # Draw temperature
            temperature_text = f"{weather_temperature:.2f}°F"
            temperature_surface = config.font.render(temperature_text, True, (255, 255, 255))

            # Position the temperature text and draw (bottom right corner)
            temp_rect = temperature_surface.get_rect()
            temp_rect.bottomright = (590, 458)
            screen.blit(temperature_surface, temp_rect)

            # Call the circle of hearts function
            images.draw_circle_of_hearts(screen, heart_image, num_hearts, radius, angle_offset)

            # Call the draw timer function
            messages.draw_timer(screen, local_time, current_message, current_temperature)

            # Draw the play button
            images.draw_play_button(screen, play_button_image)

            # Draw the song title and artist names in the top left corner
            if current_song_title is not None:
                song_title_surface = config.font.render(current_song_title, True, (255, 255, 255))
                screen.blit(song_title_surface, (10, 10))
            
            if current_artist_names is not None:
                artist_names_surface = config.font.render(current_artist_names, True, (255, 255, 255))
                screen.blit(artist_names_surface, (10, 30))

            angle_offset += 1
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    else:
        print("Failed to retrieve weather data or local time.")

    pygame.quit()

if __name__ == "__main__":
    main()