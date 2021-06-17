# Spotify Video Project by Jonathan Buchanan
# Last updated: 6/17/21
# Takes your song from spotify then brings up the youtube video. 
# Import statements
import spotipy 
import spotipy.util as util
import json
import time
import math
import lyricsgenius
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from secret import *
from sumy.summarizers.luhn import LuhnSummarizer
import collections
import spacy
import nltk
#nltk.download('punkt')

def timer(x):
    while x > 0:
        x -= 1
        print(x)
        time.sleep(1)
    return



def main():
    token = util.prompt_for_user_token(username, scope, cid, secret, redir)
    sp = spotipy.Spotify(auth=token)
    currentsong = sp.currently_playing()
    #print(currentsong['item'])
    song_name = currentsong['item']['name']
    song_artist = currentsong['item']['artists'][0]['name']
    print("Now playing {} by {}".format(song_name, song_artist))
    video = str("{} by {}".format(song_name, song_artist))
    song_length = int(math.ceil(float(currentsong['item']['duration_ms'] * .001)))
    genius = lyricsgenius.Genius(gatoken)
    #artist = genius.search_artist(song_artist, max_songs=1, sort="title")
    song = genius.search_song(song_name, song_artist)
    pattern = r'\[.*?\]'
    pattern2= r'\(.*?\)'
    lyrics = re.sub(pattern2, '', re.sub(pattern, '', song.lyrics))
    #print(lyrics)
    #print(song_length)

    parser=PlaintextParser.from_string(lyrics,Tokenizer('english'))
    #  Creating the summarizer
    luhn_summarizer=LuhnSummarizer()
    luhn_summary=luhn_summarizer(parser.document,sentences_count=1)

    search_line = str(luhn_summary[0]).split(',')[0]
    stopwords = ['-', 'the', '&', '(']
    #sp = spacy.load('en_core_web_sm')
    #spacy_stopwords = sp.Defaults.stop_words
    wordcount = {}
    for word in lyrics.lower().split():
        word = word.replace(".","")
        word = word.replace(",","")
        word = word.replace(":","")
        word = word.replace("\"","")
        word = word.replace("!","")
        word = word.replace("â€œ","")
        word = word.replace("â€˜","")
        word = word.replace("*","")
        if (word not in stopwords):# and (word not in spacy_stopwords):
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    # Print most common word
    n_print = 10
    print("\nOK. The {} most common words are as follows\n".format(n_print))
    word_counter = collections.Counter(wordcount)
    words_list = []
    for word, count in word_counter.most_common(n_print):
        words_list.append(word)
        print(word, ": ", count)

    # Adblock
    #hop = webdriver.ChromeOptions()
    #chop.add_extension('Adblock-Plus_v1.4.1.crx')
    # Create Browser
    '''
    driver = webdriver.Chrome(ChromeDriverManager().install()) #, chrome_options=chop)

    driver.maximize_window()

    wait = WebDriverWait(driver, 5)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located

    # Navigate to url with video being appended to search_query
    driver.get('https://www.youtube.com/results?search_query={}'.format(search_line))
    time.sleep(5)
    # Play the video.
    wait.until(visible((By.ID, "video-title")))
    driver.find_element_by_id("video-title").click()
    timer(song_length)
    '''
    return

# Initate
if __name__ == "__main__":
    main()