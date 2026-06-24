import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def train_local_model():
    # 1. Charger le dataset
    df = pd.read_csv('train.csv')
    
    # Nettoyage rapide (enlever les lignes vides)
    df = df.dropna(subset=['Context', 'Response'])

    # 2. Vectorisation (Transformer le texte en données mathématiques)
    vectorizer = TfidfVectorizer(stop_words='english') # ou 'french' selon ton dataset
    X = vectorizer.fit_transform(df['Context'])

    # 3. Sauvegarder le vectorizer et les données pour Django
    joblib.dump(vectorizer, 'vectorizer.pkl')
    joblib.dump(X, 'vectorized_context.pkl')
    joblib.dump(df, 'dataframe.pkl')
    print("✅ Modèle local entraîné et sauvegardé !")

if __name__ == "__main__":
    train_local_model()