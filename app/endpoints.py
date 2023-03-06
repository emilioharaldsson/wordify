from app import app
from app.wordify import generate_user_story, get_top_songs_lyrics, get_recently_listened_song_lyrics, test_Spotipy

@app.route('/top-artist-story')
def top_artist_story():
    lyrics = get_top_songs_lyrics()
    return {"story" : generate_user_story(lyrics)}


@app.route('/recently-listened-story')
def recent_listened_story():
    lyrics = get_recently_listened_song_lyrics()
    return {"story" : generate_user_story(lyrics)}


 # tests
@app.route('/test-spotify')
def test():
    res = test_Spotipy()
    return res

