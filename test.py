from app.wordify import get_raw_genius_lyrics, get_top_songs_lyrics
from app.helper import get_most_used_words, prepare_openai_prompt
from app.config import MainConfig
import openai
import os

# track = {
#     "track-name": "Pro Freak",
#     "artist": [
#         "Smino"
#     ]
# }

# lyrics = get_raw_genius_lyrics(track)['lyrics']

# words = get_most_used_words(lyrics)

# prompt = prepare_openai_prompt(words)

# openai.api_key = MainConfig.OPENAI_API_KEY

# story = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=400, temperature=0.7)['choices'][0]['text']

# print(story)

 