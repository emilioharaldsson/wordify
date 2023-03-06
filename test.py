from app.wordify import get_raw_genius_lyrics, get_top_songs_lyrics, get_recently_listened_song_lyrics, test_recently_spotify
from app.helper import get_most_used_words, prepare_openai_prompt
from app.config import MainConfig
import openai
import os
import json

