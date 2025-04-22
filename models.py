import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

# Paths to save trained artifacts
dir_path = os.path.dirname(__file__)
MODELS_DIR = os.path.join(dir_path, 'models')
VECT_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')
MODEL_PATH = os.path.join(MODELS_DIR, 'classifier.pkl')


def train_model(data_path: str):
    """
    Train a classification model on the provided CSV dataset.
    Expects `data_path` CSV with columns `email` and `type`.
    """
    df = pd.read_csv(data_path)
    # Use 'email' column for text and 'type' column for labels
    X = df['email'].values
    y = df['type'].values

    # Text vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    # Train an SVM classifier
    model = SVC(probability=True)
    model.fit(X_vec, y)

    # Save artifacts
    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(VECT_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)


def classify_email_text(text: str) -> str:
    """
    Load saved vectorizer and model to classify a single email.
    """
    if not os.path.exists(VECT_PATH) or not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model artifacts not found. Please run train_model() first.")

    with open(VECT_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    X_vec = vectorizer.transform([text])
    return model.predict(X_vec)[0]