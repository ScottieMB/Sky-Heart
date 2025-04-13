import random
import config
from datetime import datetime

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
    
# Function to draw the countdown timer and messages
def draw_timer(screen, current_message, current_temperature):
    remaining_time = config.target_date - datetime.now()
    days, seconds = remaining_time.days, remaining_time.seconds
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    seconds = seconds % 60

    # Create a formatted string for the timer
    timer_text = f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"
    timer_surface = config.font.render(timer_text, True, (255, 255, 255))  # Render text

    # Get the width and height of the timer surface
    text_width = timer_surface.get_width()
    text_height = timer_surface.get_height()

    # Calculate the position to center the text
    x_position = (config.WIDTH - text_width) // 2
    y_position = (config.HEIGHT - text_height) // 2

    # Draw the timer at the calculated position
    screen.blit(timer_surface, (x_position, y_position))

    # Draw temperature message in the bottom right (parameters are (message, text-smoothing, color))
    message_surface2 = config.font.render(current_temperature, True, (255, 255, 255))

    # Draw the random message above the timer
    message_surface = config.font.render(current_message, True, (255, 255, 255))

    # Get the width and height of the message surface
    message_width = message_surface.get_width()
    message_height = message_surface.get_height()
    message2_width = message_surface2.get_width()
    message2_height = message_surface2.get_height()

    # Calculate the position to center the message above the timer
    message_x_position = (config.WIDTH - message_width) // 2  # Center horizontally
    message_y_position = y_position - message_height - 10  # Position above the timer with some spacing

    # Calculate to be next to the weather icon
    message2_x_position = (config.WIDTH - message2_width - 12)
    message2_y_position = (config.HEIGHT - message2_height - 12)

    # Draw the message at the calculated position
    screen.blit(message_surface, (message_x_position, message_y_position))

    screen.blit(message_surface2, (message2_x_position, message2_y_position))