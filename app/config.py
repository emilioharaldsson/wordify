import os

base_dir = os.path.abspath(os.path.dirname(__file__))




class MainConfig:
    '''
    Main app configurations 
    '''
    CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    SPOTIPY_REDIRECT_URI = os.environ.get('SPOTIPY_REDIRECT_URI')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GENIUS_TOKEN = os.environ.get('GENIUS_ACCESS_TOKEN')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    



    