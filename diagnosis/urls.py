from django.urls import path
from .views import predict_intent, update_feedback, transcribe_audio

urlpatterns = [
    path('api/chat/', predict_intent, name='predict_intent'),
    path('api/transcribe_audio/', transcribe_audio, name='transcribe_audio'),
    path('api/feedback/<int:message_id>/', update_feedback, name='update_feedback'),
]
 