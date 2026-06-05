import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

song_name = input("곡 이름을 입력하세요: ")
results = sp.search(q=song_name, type='track', limit=1)

track = results['tracks']['items'][0]

print(f"\n🎵 {track['name']}")
print(f"아티스트: {track['artists'][0]['name']}")
print(f"앨범: {track['album']['name']}")
print(f"발매일: {track['album']['release_date']}")
print(f"인기도: {track.get('popularity', 'N/A')}/100")
print(f"미리듣기: {track.get('preview_url', '없음')}")

import sqlite3

# DB 연결 (없으면 자동 생성)
conn = sqlite3.connect("music.db")
cursor = conn.cursor()

# 테이블 만들기
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

# 검색 결과 저장
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
print("✅ DB에 저장 완료!")