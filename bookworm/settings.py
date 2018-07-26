"""
Django settings for bookworm project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from __future__ import absolute_import

import os
import datetime
import environ

from celery.schedules import crontab

# from authentication.tasks import task_get_user_secret_key


env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iwph6-z$cg1c(0^b&n#g1!tt*zt-j7i@m=#ckuf1u)w-qt!8%*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'rest_framework',
    'django_filters',
    # Local apps
    'authentication.apps.AuthenticationConfig',
    'books.apps.BooksConfig',
    'meta_info.apps.MetaInfoConfig',
    'file_store.apps.FileStoreConfig',
    'posts.apps.PostsConfig',
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

ROOT_URLCONF = 'bookworm.urls'

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

WSGI_APPLICATION = 'bookworm.wsgi.application'

# Load fixtures from directories list

FIXTURE_DIRS = (
   os.path.join(BASE_DIR, '/books/fixtures'),
)


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if 'DATABASE_HOST' in os.environ:
    DATABASES['default']['HOST'] = env('DATABASE_HOST')
    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    DATABASES['default']['NAME'] = env('DATABASE_NAME')
    DATABASES['default']['USER'] = env('DATABASE_USER')
    DATABASES['default']['PASSWORD'] = env('DATABASE_PASSWORD')


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Django rest framework configurations
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions',
        'rest_framework.permissions.IsAuthenticated',
    ],

    # Only allow Token Authentication for API in production
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),

    # ... other configurations
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
    )
}

JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

    'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

    'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'authentication.tasks.jwt_response_payload_handler',

    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_GET_USER_SECRET_KEY': 'authentication.tasks.task_get_user_secret_key',
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS512',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,

    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_AUTH_COOKIE': None,
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'apiKey': {
            'type': 'apiKey',
            'description': 'Personal API Key authorization',
            'name': 'Authorization',
            'in': 'header',
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


# Celery Configurations
# Celery & Broker settings

CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq"
CELERY_RESULTS_BACKEND = "amqp://guest:guest@rabbitmq"

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'


# Celery cron scheduling

CELERY_BEAT_SCHEDULE = {
    'send_sms_alert': {
        'task': 'alerts.tasks.send_sms_alert',
        'schedule': crontab(minute='15', hour='19'),
    },
}


# Django celery results configurations
CELERY_RESULT_BACKEND = 'django-db'


# SMS Service credentials
SMS_URL = env('SMS_URL', default="https://textbelt.com/text")
SMS_TOKEN = env('SMS_TOKEN', default="textbelt")


# Hash field salts and alphabet
HASHID_FIELD_SALT = env(
    'HASHID_FIELD_SALT',
    default='kj~*=b1)VJ^yO*~5qKc2U3AXqk|P/4YuD4bs+2@1.N.^HQO&u7',
)
HASH_FIELD_ALPHABET = env(
    'HASH_FIELD_ALPHABET',
    default='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
)
SALT_AUTHENTICATION_CONTACTMETHOD = env(
    'SALT_AUTHENTICATION_CONTACTMETHOD',
    default='K0jiY1y/MgN;zI06q|ffJSzjQ"U9`C+=',
)
SALT_AUTHENTICATION_PROFILE = env(
    'SALT_AUTHENTICATION_PROFILE',
    default='l6P=[!*eDzqt7eG5@k>wfAh@R-UH?l5x',
)
SALT_AUTHENTICATION_AUTHOR = env(
    'SALT_AUTHENTICATION_AUTHOR',
    default='IPc8v6ZbP;RKZ:Z|uw8=T!2yZLxtyPs5',
)
SALT_AUTHENTICATION_PROFILESETTING = env(
    'SALT_AUTHENTICATION_PROFILESETTING',
    default='W3>;@=ub(!k&a]n+OT~l_C8GqLHzm42e',
)
SALT_AUTHENTICATION_INVITATION = env(
    'SALT_AUTHENTICATION_INVITATION',
    default='XF5&39(7cM~,o4JQz6D.{.xbqvE_W4^b',
)
SALT_AUTHENTICATION_CIRCLE = env(
    'SALT_AUTHENTICATION_CIRCLE',
    default='ODB13"B/A!8]0w?m_7Dt(Li+!:C{-!}E',
)
SALT_AUTHENTICATION_CIRCLESETTING = env(
    'SALT_AUTHENTICATION_CIRCLESETTING',
    default='R;aU-Y.v_,nw8O+/2e!sMLy5m$=A6cbC',
)
SALT_AUTHENTICATION_TOKEN = env(
    'SALT_AUTHENTICATION_TOKEN',
    default='GlL_.!6RcTyu2|HhEw1k]7O~-V;Imads',
)
SALT_BOOKS_BOOK = env(
    'SALT_BOOKS_BOOK',
    default='p^oE*^4(%7;Yb:p_5Nuccz3-H?>wYJ4c',
)
SALT_BOOKS_BOOKPROGRESS = env(
    'SALT_BOOKS_BOOKPROGRESS',
    default='KTEVvVde#Z*mO;db;e1I.5T]aVwUZN"1',
)
SALT_BOOKS_BOOKCHAPTER = env(
    'SALT_BOOKS_BOOKCHAPTER',
    default='oJI94-Ej+ylQ.lqxRIc`Y5!2_{_Q=zGh',
)
SALT_BOOKS_READINGLIST = env(
    'SALT_BOOKS_READINGLIST',
    default='cF6/9w*hf.1xWzqmleOlY}>,!iWl;2@i',
)
SALT_BOOKS_BOOKREVIEW = env(
    'SALT_BOOKS_BOOKREVIEW',
    default='p6|v5qADW64CC<-4gMTnFh/N7.sV,wPG',
)
SALT_BOOKS_CONFIRMREADQUESTION = env(
    'SALT_BOOKS_CONFIRMREADQUESTION',
    default='L>fZ(XHL?!do[BlbGFIdA99fzkY;k!=+',
)
SALT_BOOKS_CONFIRMREADANSWER = env(
    'SALT_BOOKS_CONFIRMREADANSWER',
    default='JBKvt+AzL@mRF*^zw.9U$5;pnTFl[665',
)
SALT_BOOKS_READ = env(
    'SALT_BOOKS_READ',
    default='M&!_eO>;`ZIO&nnUHH*,*-#3:P&0KD]$',
)
SALT_METAINFO_TAG = env(
    'SALT_METAINFO_TAG',
    default='F3<_/,p7x*|0`1N;!ug]UmQ(G"Y5SH8[',
)
SALT_METAINFO_HASHEDTAG = env(
    'SALT_METAINFO_HASHEDTAG',
    default='dVhoQ/H5CLf*7bmNYPk4"`TZlRtwJ@3W',
)
SALT_METAINFO_METAINFO = env(
    'SALT_METAINFO_METAINFO',
    default='jZ/TE5>gnCerRiy<+U`8p&D9otm2c^C&',
)
SALT_METAINFO_LANGUAGETAG = env(
    'SALT_METAINFO_LANGUAGETAG',
    default='ZH_N/YK26txcVPFvSo^J7+$j8?aMmksq',
)
SALT_METAINFO_LOCATIONTAG = env(
    'SALT_METAINFO_LOCATIONTAG',
    default='X;Iq2*HJp+Bn,o7`P[!"<uK]ybdf#Q%8',
)
SALT_METAINFO_LOCALISETAG = env(
    'SALT_METAINFO_LOCALISETAG',
    default='l!?"pzK*2|`n81EW&-+#mPJeNyu>0o6[',
)
SALT_POSTS_EMOTE = env(
    'SALT_POSTS_EMOTE',
    default='cioP>D^|E*21?"R5&.)rg[8,W@76+VUu',
)
SALT_POSTS_POST = env(
    'SALT_POSTS_POST',
    default='g5t|Q)XG3%$@fen9UlE4:BShuqW=]jH2',
)
SALT_FILESTORE_IMAGE = env(
    'SALT_FILESTORE_IMAGE',
    default='Hh$MXf2y2Cgoj~=lYL!BP;*n8!CZ4Iw6',
)
SALT_FILESTORE_DOCUMENT = env(
    'SALT_FILESTORE_DOCUMENT',
    default='kA&F$R`q5`38fc^ZF;Hn3~x-K~-@m:P(',
)


AES_KEY_AUTHENTICATION = env(
    'AES_KEY_AUTHENTICATION',
    default='EMI164xKw7lQhmCGuH82DXtgFvbnV9yO',
)
AES_IV456_AUTHENTICATION = env(
    'AES_IV456_AUTHENTICATION',
    default='U\x80\x83&\x97\xb29\x07\xc9\x17\xb6\xcak0\x11\xb9',
)

TOKEN_RANDOM_KEY_LENGTH = env.int('TOKEN_RANDOM_KEY_LENGTH', default=32)
TOKEN_RANDOM_VALUE_LENGTH = env.int('TOKEN_RANDOM_VALUE_LENGTH', default=64)
TOKEN_SALT_START = env(
    'TOKEN_SALT_START',
    default='Kx(62Q~o0kjRyl|_sr1<*z8+.HN>b/5ci4LtMqmT,Y3@^`fJEh',
)
TOKEN_SALT_END = env(
    'TOKEN_SALT_END',
    default='HDQcA&yv<^Chf2u*L>wJ]BOtW;K=9$x8Zl?Viz!7,3Xp[1.:0s',
)

INVITE_TIMEOUT = env.int(
    'INVITE_TIMEOUT',
    default=20,
)
INVITE_SELF_TIMEOUT = env.int(
    'INVITE_SELF_TIMEOUT',
    default=1,
)


DEFAULT_LANGUAGE = 'en'
DEFAULT_LOCATION = 'gb'
DEFAULT_LOCALISATION = f'{DEFAULT_LANGUAGE}-{DEFAULT_LOCATION}'

PROFILE_TYPE_ELEVATED__MIN = 1
PROFILE_TYPE_ADMIN__MIN = 2

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='bookworm')
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {'Cache-Control': 'max-age=86400', }
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage' \
    if AWS_ACCESS_KEY_ID else \
    'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage' \
    if AWS_ACCESS_KEY_ID else \
    'django.contrib.staticfiles.storage.StaticFilesStorage'
# these next two aren't used, but staticfiles will complain without them
STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/' \
    if AWS_ACCESS_KEY_ID else '/static/'
STATIC_ROOT = '' if AWS_ACCESS_KEY_ID else None

# Load local environment specific settings
try:
    from local_settings import *
except ImportError:
    pass
