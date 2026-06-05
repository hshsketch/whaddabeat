from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Connect to Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

@app.route("/", methods=["GET", "POST"])
def index():
    track = None
    if request.method == "POST":
        song_name = request.form["song_name"]
        results = sp.search(q=song_name, type='track', limit=1)
        if results['tracks']['items']:
            track = results['tracks']['items'][0]

            # Save to database
            conn = sqlite3.connect("music.db")
            cursor = conn.cursor()
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
            conn.commit()
            conn.close()

    return render_template("index.html", track=track)

if __name__ == "__main__":
    app.run(debug=True)
    