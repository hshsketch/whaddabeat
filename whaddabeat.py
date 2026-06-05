import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Connect to Spotify API using client credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

# Get song name from user input
song_name = input("Enter a song name: ")

# Search for the track on Spotify (returns top 1 result)
results = sp.search(q=song_name, type='track', limit=1)

# Extract track information from search results
track = results['tracks']['items'][0]

# Display track details
print(f"\n🎵 {track['name']}")
print(f"Artist: {track['artists'][0]['name']}")
print(f"Album: {track['album']['name']}")
print(f"Release Date: {track['album']['release_date']}")
print(f"Popularity: {track.get('popularity', 'N/A')}/100")
print(f"Preview: {track.get('preview_url', 'Not available')}")

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("music.db")
cursor = conn.cursor()

# Create songs table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        artist TEXT,
        album TEXT,
        release_date TEXT,
        popularity INTEGER
    )
""")

# Insert search result into the database
cursor.execute("""
    INSERT INTO songs (title, artist, album, release_date, popularity)
    VALUES (?, ?, ?, ?, ?)
""", (
    track['name'],
    track['artists'][0]['name'],
    track['album']['name'],
    track['album']['release_date'],
    track.get('popularity', 0)
))

# Save changes and close connection
conn.commit()
conn.close()
print("✅ Successfully saved to database!")