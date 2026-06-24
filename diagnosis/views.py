import os
import time
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from groq import Groq  # Import du client Groq
from django.conf import settings
 

# --- CONFIGURATION DE L'IA GENERATIVE (GROQ) ---
# Chargement de la clé API depuis les variables d'environnement
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# Consignes comportementales strictes pour l'IA
SYSTEM_PROMPT = """
- répondre avec empathie
- donner des conseils simples
- proposer des exercices pratiques
- ne jamais faire de diagnostic médical
- répondre en français
"""

@api_view(['POST'])
@permission_classes([AllowAny])
def predict_intent(request):
    # Démarrage du chronomètre pour la métrique de performance
    start_time = time.time()
    
    user_text = request.data.get('message', '')
    if not user_text:
        return Response({"text": "Je vous écoute..."}, status=200)

    try:
        # Appel à l'API de génération Groq (Modèle Meta Llama 3.1)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_text,
                }
            ],
            model="llama-3.1-8b-instant",  # Le modèle le plus rapide et adapté
            temperature=0.7,               # Température pour une réponse humaine et stable
            max_tokens=150                 # Sécurité physique pour empêcher les longs textes
        )

        # Extraction de la réponse générée par l'IA
        bot_answer = chat_completion.choices[0].message.content.strip()
        
        # Calcul de la latence (temps de réponse global du backend en millisecondes)
        latency = round((time.time() - start_time) * 1000, 2)

        return Response({
            "text": bot_answer,
            "intent": "Génération IA (Llama 3.1 via Groq)",
            "metrics": {
                "latency_ms": latency,
                "model": "llama-3.1-8b-instant",
                "status": "Success"
            }
        })

    except Exception as e:
        print(f"⚠️ Erreur critique Groq API : {e}")
        return Response({
            "text": "Désolée, je rencontre une petite surcharge d'émotions techniques. Réessayez dans un instant.",
            "metrics": {"status": "Error", "details": str(e)}
        }, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def update_feedback(request, message_id):
    """Endpoint conservé pour éviter de casser les requêtes de feedback de l'interface React"""
    return Response({"status": "success"})


@api_view(['POST'])
@permission_classes([AllowAny]) # On s'assure que l'application mobile puisse y accéder librement
def transcribe_audio(request):
    if 'audio' not in request.FILES:
        return Response({'error': 'Aucun fichier audio fourni'}, status=400)
    
    try:
        audio_file = request.FILES['audio']
        
        # Appel direct à l'API Whisper de Groq en lui passant le fichier
        transcription = client.audio.transcriptions.create(
            file=(audio_file.name, audio_file.read()),
            model="whisper-large-v3",
            language="fr" # Force Whisper à transcrire et comprendre en français
        )
        
        # Récupération du texte dicté par le patient
        text_transcribed = transcription.text
        print(f"🎙️ Audio transcrit avec succès : {text_transcribed}")

        return Response({'transcribed_text': text_transcribed}, status=200)

    except Exception as e:
        print(f"⚠️ Erreur lors de la transcription Whisper : {e}")
        return Response({
            'error': 'Échec de la transcription audio.',
            'details': str(e)
        }, status=500)