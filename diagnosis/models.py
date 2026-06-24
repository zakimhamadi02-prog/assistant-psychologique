from django.db import models
from django.contrib.auth.models import User

# --- PARTIE 1 : SYSTÈME DE QUESTIONNAIRE (Arbre de décision) ---
class Question(models.Model):
    identifier = models.CharField(max_length=100, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.identifier

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    label = models.CharField(max_length=50)
    next_question_identifier = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.label} (vers {self.next_question_identifier})"

# --- PARTIE 2 : SYSTÈME DE CHAT IA (Historique & Apprentissage) ---
class Conversation(models.Model):
    # Lier la conversation à l'utilisateur connecté
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations", null=True)
    user_message = models.TextField()
    translated_message = models.TextField()
    bot_response = models.TextField()
    intent_tag = models.TextField()
    confidence = models.FloatField()
    language = models.CharField(max_length=10, default='fr') 
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Champ pour le futur feedback (Apprentissage par renforcement)
    is_correct = models.BooleanField(null=True, blank=True) 

    def __str__(self):
        return f"Chat {self.user} - {self.intent_tag} ({self.created_at})"