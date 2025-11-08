import nltk
from nltk import word_tokenize, download
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Ensure that the necessary NLTK resources are downloaded
nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4') 
nltk.download('averaged_perceptron_tagger_eng')

# Function to tokenize text
def tokenize_text(text):
    word_tokenized = word_tokenize(text)
    return word_tokenized
sentence = input("Enter a sentence: ")
tokens = tokenize_text(sentence)

print(f"Tokenized Words:", tokens) 

# Function to remove stopwords
from nltk.corpus import stopwords

nltk.download('stopwords')
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens
filtered_tokens = remove_stopwords(tokens)
print("Filtered Tokens (Stopwords Removed):", filtered_tokens)

# Stemming the tokens
def stem_text(sentence):
    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    tokens = tokenize_text(sentence)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

stemmed = stem_text(sentence)
print(f"Stemmed Words:", stemmed)  

# Part of speech tagging and lemmatization
tagged_tokens = pos_tag(tokens)

def get_wordnet_pos(tag):
    if tag.startswith('J'):  
        return 'a'
    elif tag.startswith('V'):  
        return 'v'
    elif tag.startswith('N'):  
        return 'n'
    elif tag.startswith('R'):  
        return 'r'
    else:
        return 'n'  

lemmatized_sentence = []

for word, tag in tagged_tokens:
    if word.lower() == 'are' or word.lower() in ['is', 'am']:
        lemmatized_sentence.append(word)  
    else:
        lemmatizer = WordNetLemmatizer()
        lemmatized_sentence.append(lemmatizer.lemmatize(word, get_wordnet_pos(tag)))

print("Original Sentence: ", sentence)
print("Lemmatized Sentence: ", ' '.join(lemmatized_sentence))


from sklearn.feature_extraction.text import CountVectorizer
# Bag of Words implementation
def bag_of_words(sentences):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(sentences)
    return X.toarray(), vectorizer.get_feature_names_out()

# Example usage of Bag of Words
sentences = ["This is a sample sentence.", "This is another example sentence."]
bow_array, feature_names = bag_of_words(sentences)

print("Bag of Words Array:\n", bow_array)
print("Feature Names:", feature_names)


from sklearn.feature_extraction.text import TfidfVectorizer
# TF-IDF implementation
def tfidf_vectorization(sentences):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    return X.toarray(), vectorizer.get_feature_names_out()
# Example usage of TF-IDF
sentences = ["This is a sample sentence.", "This is another example sentence."]
tfidf_array, tfidf_feature_names = tfidf_vectorization(sentences)
print("TF-IDF Array:\n", tfidf_array)
print("TF-IDF Feature Names:", tfidf_feature_names)


