"""
Django settings for CoworkingDB project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/

Do not change this file.  To change values of these
settings move the settings you want to change to a
file named local_settings.py
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'PRIVATE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# The Base URL for this application
BASE_URL = "https://example.com"

SITE_NAME = "The CRDB Project"

LOGIN_URL = "/login/"

LOGOUT_REDIRECT_URL = "home"

# Email settings
SERVER_EMAIL = "coredb@example.com"
EMAIL_HOST = "smtp.example.com"
EMAIL_HOST_USER = "admin@example.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_SUBJECT_PREFIX = "[CRDB] "

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'en'
TIME_ZONE = "America/Vancouver"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'coredb.Person'

ROOT_URLCONF = 'coredb.urls'

WSGI_APPLICATION = 'coredb.wsgi.application'

INSTALLED_APPS = [
    'coredb',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
AUTHENTICATION_BACKENDS = (
    'coredb.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

# Load the local settings file
if os.path.isfile('coredb/local_settings.py'):
    from .local_settings import *
else:
    print("No local settings file found")
