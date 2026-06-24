from sentence_transformers import SentenceTransformer
import pandas as pd
import joblib
import os

def train_v2():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(BASE_DIR, 'train.csv')).dropna(subset=['Context', 'Response'])
    
    print("Chargement du modèle de compréhension (SBERT)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Calcul des vecteurs de sens (cela peut prendre 1-2 min)...")
    # On transforme tout le dataset en vecteurs de sens
    embeddings = model.encode(df['Context'].tolist(), show_progress_bar=True)
    
    print("Sauvegarde...")
    joblib.dump(model, 'semantic_model.pkl')
    joblib.dump(embeddings, 'embeddings.pkl')
    joblib.dump(df, 'dataframe.pkl')
    print("✅ Terminé ! Pandora est maintenant beaucoup plus intelligente.")

if __name__ == "__main__":
    train_v2()