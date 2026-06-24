import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

# 1. Charger les données
with open('json_psy.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

patterns = []
tags = []
responses = {}

# EXTRACTION CORRECTE (C'est ici que ça bloquait)
for intent in data['intents']:
    tag = intent['tag']
    responses[tag] = intent['responses']
    for pattern in intent['patterns']:
        patterns.append(pattern.lower()) # On met tout en minuscule dès le départ
        tags.append(tag)

# 2. Pipeline ML Robuste
model = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
    ('clf', SVC(kernel='linear', probability=True))
])

# 3. Entraînement
model.fit(patterns, tags)

# 4. Sauvegarde
joblib.dump(model, 'mental_health_model.pkl')
joblib.dump(responses, 'responses.pkl')

print(f"✅ Modèle entraîné avec {len(patterns)} phrases et {len(responses)} catégories !")