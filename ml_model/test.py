import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import feature_extraction, linear_model, model_selection, preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score
import string
from nltk.corpus import stopwords
import nltk
import gensim
import spacy
import joblib


def punctuation_removal(text):
    all_list = [char for char in text if char not in string.punctuation]
    clean_str = ''.join(all_list)
    return clean_str


def stop_words_removal(text):
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])
    result = []
    for token in gensim.utils.simple_preprocess(text, min_len=3):
        if token not in gensim.parsing.preprocessing.STOPWORDS and token not in stop_words:
            if token.isdigit() or token.isdecimal():
              result.append("D"*len(token))
            else:
              result.append(token)
            
    return ' '.join(result)


def preprocess(text):
    X_test = pd.DataFrame([text], columns=["text"])
    X_test['text'] = X_test['text'].apply(punctuation_removal)
    X_test['text'] = X_test['text'].apply(stop_words_removal)
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    X_test['text'] = X_test['text'].apply(lambda x: " ".join([token.lemma_ for token in nlp(x)]))
    return X_test


'''Orchestrator function - takes the article text as input and returns (prediction, confidence_score)
   prediction - 'true'/'false'
   confidence_score - float value'''
def infer_model(text):
    X_test = preprocess(text)
    X_test = X_test.iloc[0].values
    model = joblib.load('ml_model/multinb.sav')
    prediction = model.predict(X_test)
    probability = model.predict_proba(X_test)
    confidence = probability.max(axis=1)
    return (prediction[0], confidence[0])
    
    
    