import os
import string
import re
import emoji
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import en_core_web_sm

from data import *

os.environ['KMP_DUPLICATE_LIB_OK']='True'


def sentiment_analysis(pick_ayz, a_comments, symbols):
    """
    Analyzes sentiment of top pickers

    :param pick_ayz: int - top picks to analyze
    :param a_comments: dict - all the comments to analyze
    :param symbols: dict - dictionary of sorted tickers based on mentions
    :return: dict - dictionary of all the sentiment analysis
    """

    scores = {}

    vader = SentimentIntensityAnalyzer()

    # adding custom words from data.py
    vader.lexicon.update(new_words)
    picks_sentiment = list(symbols.keys())[:pick_ayz]

    for symbol in picks_sentiment:
        stock_comments = a_comments[symbol]
        for cmnt in stock_comments:
            # remove emojis
            emojiless = emoji.get_emoji_regexp().sub(u'', cmnt)

            # remove punctuation
            text_punc = "".join([char for char in emojiless if char not in string.punctuation])
            text_punc = re.sub['[0-9]+','', text_punc]

            # tokenizing and cleanning
            tokenizer = RegexpTokenizer('\w+|$[\d.]+|http\S+')
            tokenized_string = tokenizer.tokenize(text_punc)

            # converting to lower case
            lower_tokenized = [word.lower() for word in tokenized_string]

            # remove stop words
            nlp = en_core_web_sm.load()
            stopwords = nlp.Defaults.stop_words
            sw_removed = [word for word in lower_tokenized if not word in stopwords]

            # normalize the words using lematization
            lematizer = WordNetLemmatizer()
            lematizer_tokens = ([lematizer.lemmatize(w) for w in sw_removed])

            # calculating sentiment of every word in comments n comebining them
            score_cmnt = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}

            word_count = 0
            for word in lematizer_tokens:
                if word.upper() not in us:
                    score = vader.polarity_scores(word)
                    word_count+=1
                    for key, _ in score.items():
                        score_cmnt[key] += score[key]
                else:
                    score_cmnt['pos'] = 2.0

            # calculating avg
            # handles: ZeroDivisionError: float divsion by zero
            try:
                for key in score_cmnt:
                    score_cmnt[key] = score_cmnt[key] / word_count
            except:
                pass

            # adding score the specific symbol
            if symbol in scores:
                for key, _ in score_cmnt.items():
                    scores[symbol][key] += score_cmnt[key]
            else:
                scores[symbol] = score_cmnt

        # calculating avg
        for key in score_cmnt:
            scores[symbol][key] = scores[symbol][key] / symbols[symbol]
            scores[symbol][key] = "{pol:.3f}".format(pol=scores[symbol][key])

    return scores