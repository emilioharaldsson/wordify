from app import app
from app.wordify import generate_user_story, get_top_songs_lyrics, get_recently_listened_song_lyrics, test_Spotipy, test_recently_spotify, test_top_spotify

@app.route('/top-artist-story', methods=['GET'])
def top_artist_story():
    lyrics = get_top_songs_lyrics()
    return {"story" : generate_user_story(lyrics)}

@app.route('/recently-listened-story', methods=['GET'])
def recent_listened_story():
    lyrics = get_recently_listened_song_lyrics()
    return {"story" : generate_user_story(lyrics)}

 # tests
@app.route('/test-spotify')
def test():
    res = test_Spotipy()
    return res

@app.route('/test-spotify-v2')
def test_v2():
    res = test_recently_spotify()
    return res

@app.route('/test-spotify-v3')
def test_v3():
    res = test_top_spotify()
    return res

