import spacy
import pandas as pd
from nltk.tokenize import word_tokenize
pd.set_option('display.max_columns', None)

nlp = spacy.load("en_core_web_sm")

# https://spacy.io/usage/linguistic-features

def print_linguistic_features(text):
    tokens = word_tokenize(text)
    doc = nlp("".join(cake_wikipedia))

    data = {'Text':[token.text for token in doc], 'Lemma':[token.lemma_ for token in doc], 'Part-of-speech':[token.pos_ for token in doc], 'Dependency':[token.dep_ for token in doc], 'Shape':[token.shape_ for token in doc], 'Is Alpha':[token.is_alpha for token in doc], 'Stopword':[token.is_stop for token in doc]}
    df = pd.DataFrame (data, columns = ['Text', 'Lemma', 'Part-of-speech', 'Dependency', 'Shape', 'Is Alpha', 'Stopword'])

def show_tokens(tokens, T=True):
    data = {'Text': tokens}
    df = pd.DataFrame(data, columns = ['Text'])
    if T:
        return df.T
    else:
        return df


def show_lemmas(original, lemmas, T=True):
    data = {'Lemmas': lemmas, 'Text':original}
    df = pd.DataFrame(data, columns = ['Text', 'Lemmas'])
    if T:
        return df.T
    else:
        return df
        
