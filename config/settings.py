"""
Django settings for config project - Pandora AI
Optimisé pour le déploiement Railway
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charge les variables d'environnement depuis .env (local)
# Sur Railway, elles seront définies directement dans le dashboard
load_dotenv()

# =============================================
# CHEMINS
# =============================================
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================
# SÉCURITÉ
# =============================================
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-9bq^*pauu)hxv#46w)f&ka5zg*ebqz96l1eus6u&^%y9zvx+&k'
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']  # Railway gère le domaine

# =============================================
# APPLICATIONS
# =============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'diagnosis',
]

# =============================================
# MIDDLEWARE
# =============================================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        # ← EN PREMIER obligatoire
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← fichiers statiques Railway
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# =============================================
# TEMPLATES
# =============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =============================================
# BASE DE DONNÉES
# =============================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# =============================================
# VALIDATION MOTS DE PASSE
# =============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================
# INTERNATIONALISATION
# =============================================
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Casablanca'
USE_I18N = True
USE_TZ = True

# =============================================
# FICHIERS STATIQUES (WhiteNoise pour Railway)
# =============================================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================
# UPLOADS / FICHIERS AUDIO
# =============================================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Taille max fichier audio : 10MB (pour Whisper)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760

# =============================================
# CORS (React Native + React Web)
# =============================================
CORS_ALLOW_ALL_ORIGINS = True  # Autorise toutes les origines (mobile inclus)

CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# =============================================
# REST FRAMEWORK
# =============================================
REST_FRAMEWORK = {
    # Désactivé pour les endpoints Pandora (AllowAny dans views.py)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',  # ← Mobile n'a pas de JWT
    ),
}

# =============================================
# JWT
# =============================================
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# =============================================
# CLÉ GROQ (depuis variable d'environnement)
# =============================================
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')

# =============================================
# CLÉS PAR DÉFAUT
# =============================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'