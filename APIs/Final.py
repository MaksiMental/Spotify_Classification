import os
import time
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

THROTTLE_TIME = 2 # Seconds

def get_track_features(track_id, genre):
    # Check if we've already processed this track
    if track_id in processed_tracks:
        return None

    meta = sp.track(track_id)
    features = sp.audio_features(track_id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    valence = features[0]['valence']

    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, key, valence, genre]

    # Add the track ID to our set of processed tracks
    processed_tracks.add(track_id)

    return track

def get_genre_tracks(genre, limit=45):
    tracks = []
    results = sp.search(q='genre:"{}"'.format(genre), limit=limit, type='track')
    for item in results['tracks']['items']:
        track_id = item['id']
        track = get_track_features(track_id, genre)
        if track is not None:
            tracks.append(track)
        time.sleep(THROTTLE_TIME)  # Throttle requests
    return tracks

if __name__ == "__main__":
    genres = ["pop", "rock", "jazz", 'edm', 'country', 'latin', 'hip hop', 'reggae', 'funk', 'blue', 'folk', 'soul']  
    all_tracks = []
    processed_tracks = set()  # Keep track of the tracks we've processed

    while len(all_tracks) < 10000:
        for genre in tqdm(genres):
            tracks = get_genre_tracks(genre)
            all_tracks.extend(tracks)
            if len(all_tracks) >= 10000:
                break

    # create dataset
    df = pd.DataFrame(all_tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'key', 'valence', 'genre'])
    df.to_csv("spotify.csv", sep = ',')



 