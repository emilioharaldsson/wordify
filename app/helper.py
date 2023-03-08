import re
import nltk
# nltk.download('all')
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords, wordnet

# Handling Spotify response object
def clean_up_song_title(song_title):
    return re.sub(r'\([^()]*\)', '', song_title).strip()

def genius_json_encoder(song):
    return {"name": song.title,
            "artist_name": song.artist,
            "lyrics": song.lyrics}

def clean_list(list):
    cleaned_list = [item for item in list if item is not None]
    return cleaned_list

# Handling getting all lyrics
def accumulate_all_lyrics(tracks):
    lyric_sum = ''
    for track in tracks:
        lyric_sum += track['lyrics']
        lyric_sum += ' '
    return lyric_sum.lower()


# Parse and filter raw_lyrics for input words

def is_noun_or_adjective(word, pos):
    if pos.startswith('NN') or pos.startswith('JJ'):
        return True
    synsets = wordnet.synsets(word)
    for syn in synsets:
        if syn.pos() == 'n' or syn.pos() == 'a':
            return True
    return False

def filter_for_noun_or_adjective(text):
    '''
    Returns (string) lyrics minus unwanted parts of speech
    '''
    words = word_tokenize(text)
    pos_tagged_words = pos_tag(words)
    excluded_list =["chorus", "verse", "genius"]
    post_filter = [word for (word, pos) in pos_tagged_words if is_noun_or_adjective(word, pos) and word not in excluded_list]
    return ' '.join(post_filter)

def filter_text(text):
    words = word_tokenize(text)
    
    stop_words = set(stopwords.words('english'))
    exclude_list = set(["[", "]", "of", "AI", "ai", "a", "ta", "chorus", "verse", "is", "have", "got","from", "in", "at", "on", "for", "if", "else", "what", "how", "why", "are", "be", "you", "it", "your", "will", "that", "there", "this", "to", "was", "the-"])
    filtered_words = [word for word in words if word not in stop_words and word not in exclude_list]
    
    tagged_words = pos_tag(filtered_words)
    
    relevant_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS']
    filtered_tags = [word[0] for word in tagged_words if word[1] in relevant_tags]
    
    return filtered_tags

def get_most_used_words(raw_lyrics):
    '''
    returns list of most used words according to input lyrics
    '''
    lyrics = filter_for_noun_or_adjective(raw_lyrics)
    all_words = filter_text(lyrics)
    word_freq_chart = {}
    for word in all_words:
        if word in word_freq_chart:
            word_freq_chart[word] += 1
        else:
            word_freq_chart[word] = 1
    sorted_freq_chart = sorted(word_freq_chart.items(), key=lambda x: x[1], reverse=True)
    top_twenty_scores = sorted_freq_chart[:20]
    top_twenty_words = [word[0] for word in top_twenty_scores]
    return top_twenty_words
    
# assist with openai request

def prepare_openai_prompt(words):
    '''
    returns (string) prompt header for openai API call
    '''
    prompt_a = '''
    A sentient AI called Spooky is a talented storyteller and writer. Spooky can write unique, captivating stories that can range in genre. Given a list of 20 words, Spooky can write a story that either use the given words, or a story about these words in general. Spooky’s stories are between 250 and 750 characters long. 

    // start relevant content

    '''
    prompt_b = '''
    Given list of words: 
    '''

    prompt_c = '''
    // end of relevant content

    Spooky writes:
    '''
    template = prompt_b + ', '.join(words)

    final_prompt = prompt_a + template + prompt_c
    
    return final_prompt
