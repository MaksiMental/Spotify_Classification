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

THROTTLE_TIME = 0.50  # Seconds

def get_track_features(track_id):
    meta = sp.track(track_id)
    features = sp.audio_features(track_id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    popularity = meta['popularity']

    # Get the artist's genres
    artist_id = meta['artists'][0]['id']
    artist_meta = sp.artist(artist_id)
    genres = artist_meta['genres']

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

    track = [track_id, name, album, artist, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, key, valence, genres]
    return track

def get_playlist_tracks(playlist_id):
    tracks = []
    playlist = sp.user_playlist_tracks("spotify", playlist_id)
    for item in playlist['items']:
        track = item['track']
        track_id = track['id']
        track = get_track_features(track_id)
        tracks.append(track)
        time.sleep(THROTTLE_TIME)  # Throttle requests
    return tracks

if __name__ == "__main__":
    playlists = ['6kh8X00EqGovzCJeYyWVTJ']  # Replace with your playlist IDs 
    all_tracks = []
    for playlist in tqdm(playlists):
        tracks = get_playlist_tracks(playlist)
        all_tracks.extend(tracks)

    # create dataset
    df = pd.DataFrame(all_tracks, columns = ['track_id', 'name', 'album', 'artist', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'key', 'valence', 'genre'])
    df.to_csv("spotify_thewweknd.csv", sep = ',')
