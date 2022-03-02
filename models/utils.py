from sklearn.base import BaseEstimator, TransformerMixin
from keybert import KeyBERT
import pandas as pd
import re
import nltk

#preprocessing
#vectorization
class Preprocessor(BaseEstimator, TransformerMixin):

    #lst_stopwords = set(nltk.corpus.stopwords.words("english"))

    def __init__(self):
        self.lst_stopwords = set(nltk.corpus.stopwords.words("english"))

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        X['Job Description'] = X['Job Description'].apply(
            lambda x: utils_preprocess_text(x,
                                            flg_stemm=False,
                                            flg_lemm=True,
                                            lst_stopwords=self.lst_stopwords))
        return X


class KeywordsExtraction(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.kw_model = KeyBERT()

    def key_words(self, text):
        keywords = self.kw_model.extract_keywords(text,
                                                  keyphrase_ngram_range=(1, 2),
                                                  stop_words='english',
                                                  use_mmr=True,
                                                  diversity=0.5,
                                                  top_n=10)
        keywords = [i[0] for i in keywords]
        return keywords

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        assert isinstance(X, pd.DataFrame)
        print(X['Job Description'])
        X['KeyWords'] = X['Job Description'].apply(self.key_words)

        return X[['KeyWords']]

# X_list = [i[0] for i in X ]


def utils_preprocess_text(text,
                          flg_stemm=False,
                          flg_lemm=True,
                          lst_stopwords=None):
    ## clean (convert to lowercase and remove punctuations and characters and then strip)
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())

    #remove number
    text = re.sub('\d+', '', text)

    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]

    ## Stemming (remove -ing, -ly, ...)
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]

    ## Lemmatisation (convert the word into root word)
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    ## back to string from list
    text = " ".join(lst_text)
    return text
