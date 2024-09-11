from pathlib import Path
import os
from django.http import JsonResponse

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def my_view(request):
    if request.method == "OPTIONS":
        response = JsonResponse({'status': 'ok'})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ["*"]


# Environment Variables
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT',5432))
REDIS_HOST = os.environ.get('REDIS_HOST')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL')

# # Email variables
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT',587))
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# Email variables
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = 'alumniassociationcseduaa@gmail.com'
# EMAIL_HOST_PASSWORD = 'qizmzjbmfirpanpo'

# Application definition

INSTALLED_APPS = [
    'base',
    'users',
    'blogs',
    'events',
    'mailing',
    'payments',
    'cards',
    'rest_framework',
    'rest_framework.authtoken',
    # 'accounts',
    'drf_yasg',
    'corsheaders',
    'bs4',
    'fuzzywuzzy',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslcommerz'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://cseduaa.org',
    # 'https://localhost',
    "http://localhost:3000",
    "http://localhost:8000",
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    'http://cseduaa.org',
    # 'https://localhost',
    "http://localhost:3000",
    "http://localhost:8000",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-csrf-token",
    "x-requested-with",
]
ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'mailing/templates'
        ],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }

# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_HOST,
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

# Celery
# CELERY_BROKER_URL = RABBITMQ_URL
CELERY_BROKER_URL = REDIS_HOST
CELERY_RESULT_BACKEND = REDIS_HOST
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_DEFAULT_QUEUE = 'myproject.celery'

# SSLCommerz Configuration
SSLCOMMERZ_STORE_ID = 'tripn66a8968d7042f'
SSLCOMMERZ_STORE_PASSWORD = 'tripn66a8968d7042f@ssl'
SSLCOMMERZ_API_URL = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php'
SSLCOMMERZ_VALIDATION_URL = 'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php'
SSLCOMMERZ_SANDBOX = True

# Your domain or local testing domain
YOUR_DOMAIN = 'http://localhost:8000'

# Success, fail, cancel URLs
SSLCOMMERZ_SUCCESS_URL = f'{YOUR_DOMAIN}/payments/success/'
SSLCOMMERZ_FAIL_URL = f'{YOUR_DOMAIN}/payments/fail/'
SSLCOMMERZ_CANCEL_URL = f'{YOUR_DOMAIN}/payments/cancel/'
SSLCOMMERZ_IPN_URL = f'{YOUR_DOMAIN}/payments/ipn/'
