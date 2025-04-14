import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os
import random

# Hardcoded list of songs (format - spotify:track:(spotify ID))
songs = [
    "<your-tracks-here>"
]

def credentials():
    # Spotify credentials (OAuth 2.0)
    client_id = os.getenv('SPOTIPY_CLIENT_ID')
    client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                        client_secret=client_secret,
                                        redirect_uri="http://localhost:8080/callback",
                                        scope="user-read-playback-state user-modify-playback-state"))
    return sp
    
# Function to check if access token is expired. If it is, it'll refresh it. (Mainly in case OAuth doesn't refresh it after an hour)
def refresh_access_token(sp):
    if sp.auth_manager.is_token_expired(sp.auth_manager.get_access_token()):
        sp.auth_manager.refresh_access_token(sp.auth_manager.get_refresh_token())
        print("Access token refreshed.")
    else:
        print("Access token is still valid.")

# Function to fetch and play a random song
def play_random_song():
    # Get devices (use this for error checking)
    devices = credentials.sp.devices()
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
        credentials.sp.start_playback(device_id=device_id, uris=[song_uri])

        # Fetch track details
        track_info = credentials.sp.track(track_id)
        song_title = track_info['name'] 
        artists = track_info['artists']
        artist_names = ', '.join([artist['name'] for artist in artists])  # Join artist names

        return song_title, artist_names
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error playing song: {e}")
        return None, None