from app.config import MainConfig
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from lyricsgenius import Genius
from app.helper import clean_up_song_title, genius_json_encoder, clean_list, accumulate_all_lyrics, get_most_used_words, prepare_openai_prompt
import concurrent.futures

import openai



def create_spotipy_client(scope):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        MainConfig.CLIENT_ID, MainConfig.CLIENT_SECRET, MainConfig.SPOTIPY_REDIRECT_URI, scope=scope))
    return sp

def format_spotify_response(res):
    formatted_data = [{"track-name": clean_up_song_title(track["name"]), "uri" : track['uri'], "artist" : [artist['name'] for artist in track['artists']]} for track in res]
    return formatted_data

def test_Spotipy():
    sp = create_spotipy_client('user-top-read')
    res = sp.current_user_top_tracks(limit=2)
    return res

def get_raw_genius_lyrics(track):
    genius = Genius(MainConfig.GENIUS_TOKEN)
    response = genius.search_song(track["track-name"], track['artist'][0])
    if response is not None:
        return genius_json_encoder(response)
    else:
        print("Track not found, track skipped")

def get_top_songs_lyrics():
    '''
    returns (string) top 10 song lyrics
    '''
    sp_client = create_spotipy_client("user-top-read")
    response = format_spotify_response(sp_client.current_user_top_tracks(limit=1)['items'])
    tracks = clean_list(response)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        list_w_lyrics = list(executor.map(get_raw_genius_lyrics, tracks))
    raw_lyrics = accumulate_all_lyrics(list_w_lyrics)
    return raw_lyrics

def get_recently_listened_song_lyrics():
    '''
    returns (string) lyrics of 10 most recently listened tracks

    '''
    sp_client = create_spotipy_client("user-read-recently-played")
    response = format_spotify_response(sp_client.current_user_recently_played(limit=10))
    tracks = clean_list(response)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        list_w_lyrics = list(executor.map(get_raw_genius_lyrics, tracks))
    raw_lyrics = accumulate_all_lyrics(list_w_lyrics)
    return raw_lyrics



def generate_user_story(raw_lyrics):
    '''
    Returns (string) user story based on most-used words in top 20 spotify song lyrics
    '''
    words = get_most_used_words(raw_lyrics)
    prompt = prepare_openai_prompt(words)
    
    openai.api_key = MainConfig.OPENAI_API_KEY
    story = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=400, temperature=0.7)['choices'][0]['text']
    return story

