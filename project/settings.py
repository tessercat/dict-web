""" Django project settings. """
import ast
import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY_FILE = BASE_DIR / 'var' / 'secret_key'
if os.path.isfile(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, encoding="utf-8") as secfd:
        SECRET_KEY = secfd.read().strip()
else:
    SECRET_KEY = get_random_secret_key()
    with open(SECRET_KEY_FILE, 'w', encoding='utf-8') as secfd:
        secfd.write(SECRET_KEY)

with open(BASE_DIR / 'var' / 'settings.py', encoding='utf-8') as setfd:
    ENV = ast.literal_eval(setfd.read())

ADMINS = ENV['ADMINS']

ALLOWED_HOSTS = (
    ENV['ALLOWED_HOST'],
    'localhost'
)

SERVER_EMAIL = ENV['SERVER_EMAIL']

TIME_ZONE = ENV['TIME_ZONE']

DEBUG = False

EMAIL_SUBJECT_PREFIX = '[dictionary] '

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'dictionary.apps.DictionaryConfig',
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

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'var' / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
