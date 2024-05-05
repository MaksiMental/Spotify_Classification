import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import backoff
from spotipy import SpotifyException

# Define backoff retry conditions
def need_retry(e):
    return isinstance(e, SpotifyException) and e.http_status in [429, 500, 502, 503, 504]

@backoff.on_exception(
    backoff.expo,
    SpotifyException,
    max_tries=10,
    giveup=lambda e: not need_retry(e),
    factor=2,
    jitter=backoff.full_jitter
)
def spotify_call(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        if result is None:
            raise SpotifyException(-1, -1, 'No response from Spotify API')
        return result
    except SpotifyException as e:
        print(f"SpotifyException occurred: {e}")
        raise

# Set up Spotify API client
auth_manager = SpotifyOAuth(
    client_id='',
    client_secret='',
    redirect_uri='https://localhost:3000',
    scope='playlist-read-private playlist-read-collaborative'
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Get playlist tracks function
def get_playlist_tracks(sp, playlist_id):
    print(f"Fetching tracks from playlist: {playlist_id}")
    tracks = []
    response = spotify_call(sp.playlist_tracks, playlist_id)
    while response:
        items = response.get('items', [])
        for item in items:
            track = item.get('track')
            if track and track.get('id'):
                tracks.append({
                    'track_id': track['id'],
                    'name': track['name'],
                    'album': track['album']['name'],
                    'artist_id': track['artists'][0]['id'],
                    'artist_name': track['artists'][0]['name'],
                    'popularity': track['popularity']
                })
        # Check for the next set of tracks
        if response.get('next'):
            response = spotify_call(sp._get, response.get('next'))
        else:
            break
    return tracks

# Get audio features function
def get_audio_features(sp, track_ids):
    print("Fetching audio features...")
    audio_features = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i+50]
        batch_features = spotify_call(sp.audio_features, batch)
        audio_features.extend(batch_features if batch_features else [])
    return audio_features

# Playlist IDs to fetch tracks from
danish_playlist_ids = [
    '01LfUDruOSfEocS5uVt1FE',
]

# Fetch tracks and audio features
all_tracks = []
for pid in danish_playlist_ids:
    all_tracks.extend(get_playlist_tracks(sp, pid))

track_ids = [track['track_id'] for track in all_tracks]
audio_features = get_audio_features(sp, track_ids)

# Merge track details and audio features
tracks_with_features = []
for track, features in zip(all_tracks, audio_features):
    if features:
        track.update(features)
        tracks_with_features.append(track)

# Save to DataFrame and CSV file
df = pd.DataFrame(tracks_with_features)
selected_columns = [
    'track_id', 'name', 'album', 'artist_name', 'popularity',
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
    'duration_ms', 'time_signature'
]
df[selected_columns].to_csv('danish_hitlist_songs4.csv', index=False)
print(f"Data for {len(df)} tracks saved to 'danish_hitlist_songs.csv'")