"""Containing all functions necessary to preprocess data and load model"""
import re
import pathlib

from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

from keras.models import load_model as keras_load_model
from keras.preprocessing.sequence import pad_sequences

from api.config import MACHINE_LEARNING_OPTION as config_models

# Try to use cPickle because it works better
try:
    import cPickle as pickle
except ImportError:
    import pickle


# Global Variables
_pre_process_model = None
_score_model = None

# Some Constants
TEXT_CLEANING_RE = r"@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"
STOP_WORDS = stopwords.words("english")
STEMMER = SnowballStemmer("english")
SEQUENCE_LENGTH = 300

POSITIVE = 'POSITIVE'
NEGATIVE = 'NEGATIVE'
NEUTRAL = 'NEUTRAL'
SENTIMENT_THRESHOLDS = (0.4, 0.7)

MODELS_FOLDER = pathlib.Path(config_models('models_path'))
SCORE_MODEL = MODELS_FOLDER / config_models('score_model')
PRE_PROCESS_MODEL = MODELS_FOLDER / config_models('preprocess_model')


def load_preprocess():
    """
    Loading Preprocess Pickle using CPickle.
    """
    global _pre_process_model
    if _pre_process_model is None:
        with open(PRE_PROCESS_MODEL, 'rb') as fd:
            _pre_process_model = pickle.load(fd)
    return _pre_process_model


def load_model():
    """
    Loading Score Model using Keras load_model.
    """
    global _score_model
    if _score_model is None:
        _score_model = keras_load_model(SCORE_MODEL)
    return _score_model


def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in STOP_WORDS:
            if stem:
                tokens.append(STEMMER.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)


def decode_sentiment(score, include_neutral=True):
    if include_neutral:
        label = 'NEUTRAL'
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE
        return label
    return NEGATIVE if score < 0.5 else POSITIVE


# Now make a function to score the data!
def score(data, include_neutral=False):
    # Getting preprocess model
    # and score model. Don't need to worry
    # about receiving extra_columns because
    # the contract establishes which data will
    # be received.
    pre_process = load_preprocess()
    model = load_model()

    text = data['text']
    # Preprocess data removing special symbols
    # users and links
    pre_processed_text = preprocess(text)
    # Tokenize text
    x_text = pad_sequences(
        pre_process.texts_to_sequences([pre_processed_text]),
        maxlen=SEQUENCE_LENGTH
    )
    # Predict score
    score = model.predict([x_text])[0]
    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    # Sending back information about response data
    response_data = {
        'score': float(score),
        'label': label
    }

    return response_data
