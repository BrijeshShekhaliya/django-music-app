# core/settings.py

from pathlib import Path
import os

print("--- LOADING LATEST SETTINGS.PY FILE ---")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-h$7r2b%q+gsg1g+r4#+&@3buj0#2*b-ua@@s-ibw!z2&74e!($'

DEBUG = True
ALLOWED_HOSTS = []


# ------------------------
# Installed Apps
# ------------------------
INSTALLED_APPS = [
    # Your Apps
    'music.apps.MusicConfig',

    # Third-Party Apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cloudinary_storage',
    'cloudinary',

    # Django Built-in Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ------------------------
# Templates
# ------------------------
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Project-level templates
        'APP_DIRS': True,  # Looks inside app/templates automatically
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'music.context_processors.is_creator_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ------------------------
# Database
# ------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------------------------
# Password Validators
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------
# Internationalization
# ------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------
# Static & Media
# ------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------
# Custom User Model
# ------------------------
AUTH_USER_MODEL = 'music.CustomUser'

# ------------------------
# Authentication
# ------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',          # Django default
    'allauth.account.auth_backends.AuthenticationBackend' # Allauth
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ------------------------
# Allauth Settings (Updated for Django 5.2+)
# ------------------------

# Login methods: allow both username and email
ACCOUNT_LOGIN_METHODS = {"username", "email"}

# Signup fields (fields with * are required)
ACCOUNT_SIGNUP_FIELDS = [
    "username*",
    "email*",
    "password1*",
    "password2*",
]

# Email verification
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# Use our custom signup form
ACCOUNT_FORMS = {"signup": "music.forms.CustomSignupForm"}
LOGIN_REDIRECT_URL = "/redirect-after-login/"
