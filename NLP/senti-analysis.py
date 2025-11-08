import pandas as pd
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
nltk.download('wordnet')

#sentiment_analysis
def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment

text = input("Enter a text for sentiment analysis: ")
sentiment = sentiment_analysis(text)
print(f"Sentiment Analysis: {sentiment}")
