from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================
# SECURITY
# =========================================

SECRET_KEY = 'django-insecure-change-this-key'

DEBUG = True

ALLOWED_HOSTS = []


# =========================================
# INSTALLED APPS
# =========================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CHANNELS
    'channels',

    # YOUR APP
    'main',
]


# =========================================
# MIDDLEWARE
# =========================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =========================================
# URLS
# =========================================

ROOT_URLCONF = 'core.urls'


# =========================================
# TEMPLATES
# =========================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates',
        ],

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


# =========================================
# WSGI + ASGI
# =========================================

WSGI_APPLICATION = 'core.wsgi.application'

ASGI_APPLICATION = 'core.asgi.application'

CELERY_BROKER_URL = 'redis://localhost:6379/0'

# =========================================
# DATABASE
# =========================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =========================================
# PASSWORD VALIDATORS
# =========================================

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


# =========================================
# LANGUAGE
# =========================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# =========================================
# STATIC FILES
# =========================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


# =========================================
# DEFAULT AUTO FIELD
# =========================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =========================================
# CHANNEL LAYERS (LIVE WEBSOCKET)
# =========================================

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


# =========================================
# LOGIN REDIRECTS
# =========================================

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/dashboard/'


# =========================================
# SESSION
# =========================================

SESSION_COOKIE_AGE = 1209600
SESSION_SAVE_EVERY_REQUEST = True