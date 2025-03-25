"""
Django settings for tuotteet project.
"""

import os
from pathlib import Path

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security ===
SECRET_KEY = 'a&fhwmypj*-^010nvne69)&e^t_a9_hwkr==cu%o53=09xcyj6'
DEBUG = True
ALLOWED_HOSTS = ['0.0.0.0', 'www.xn--hyty-6qa.net', 'xn--hyty-6qa.net']

# === Applications ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',  # ensure this is before guardian
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guardian',                     # object-level permissions
    'selosteet.apps.SelosteetConfig',
    'django_extensions',     # <-- Make sure this is here
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# === Middleware ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware', # Uncomment if you use translations
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tuotteet.urls'

# === Templates ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tuotteet.wsgi.application'

# === Database ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === Password validation ===
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# === Internationalization ===
LANGUAGE_CODE = 'fi-FI'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# === Static files ===
STATIC_URL = '/selosteet/static/'
STATIC_ROOT = BASE_DIR / 'selosteet/static'

# === Login/Logout redirects ===
LOGIN_REDIRECT_URL = '/selosteet/accounts/login/'
LOGIN_URL = '/selosteet/admin/login/'

# === Security for HTTPS (optional) ===
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# === Default primary key field type (Django 3.2+) ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
