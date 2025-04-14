import requests
import io
import pygame
import os
import math
from src.config import WIDTH, HEIGHT

# Function to load the weather icon in the input city
def load_weather_icon(url):
    response = requests.get(url)
    image_data = io.BytesIO(response.content)
    image = pygame.image.load(image_data)
    return image

# Load background images based on weather condition
def load_images(weather_condition, night_time):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Load the images we need from assets
    heart_image = pygame.image.load(os.path.join(script_dir, 'assets/heart.png')).convert_alpha()
    heart_image = pygame.transform.scale(heart_image, (50, 50))
    play_button_image = pygame.image.load(os.path.join(script_dir, 'assets/play.png')) 
    play_button_image = pygame.transform.scale(play_button_image, (50, 50))

    # Decide what our background will be
    if night_time:
        background_image = pygame.image.load(os.path.join(script_dir, 'assets/nighttime.jpg'))
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

    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) 

    return background_image, heart_image, play_button_image

# Draw the play button at the specified position
def draw_play_button(screen, play_button_image):
    screen.blit(play_button_image, (590, 10))

# Function to draw the full circle of hearts
def draw_circle_of_hearts(screen, heart_image, angle_offset, num_hearts=12):
    center_x, center_y = WIDTH // 2, HEIGHT // 2  # Center of the screen
    adjusted_radius = 180 # Adjusted radius with padding
    angle_between_hearts = (360 / num_hearts)

    for i in range(num_hearts):
        # Calculate the angle for this heart in radians
        angle = math.radians(i * angle_between_hearts + angle_offset)

        # Calculate x and y position based on the angle
        heart_x = int(center_x + adjusted_radius * math.cos(angle) - heart_image.get_width() / 2)
        heart_y = int(center_y + adjusted_radius * math.sin(angle) - heart_image.get_height() / 2)

        # Rotate the heart image
        rotated_heart_image = pygame.transform.rotate(heart_image, -math.degrees(angle))

        # Get the rect of the rotated image and set its position to the center (even while it's rotating)
        rotated_rect = rotated_heart_image.get_rect(center=(heart_x + heart_image.get_width() / 2, heart_y + heart_image.get_height() / 2))

        # Draw the rotated heart image
        screen.blit(rotated_heart_image, rotated_rect.topleft)