import pygame
from datetime import datetime
import os

# Constants for the display
WIDTH, HEIGHT = 650, 500
WHITE = (255, 255, 255)

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 50, 50
button_x = WIDTH - BUTTON_WIDTH - 10  # 10 pixels from the right
button_y = 10  # 10 pixels from the top

# Timer settings
target_date = os.getenv('YOUR_DATETIME')

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the font using an absolute path
font_path = os.path.join(script_dir, 'assets/Grand9kPixel.ttf')
font = pygame.font.Font(font_path, 15)