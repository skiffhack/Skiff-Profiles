from django.conf import global_settings
import os, sys, urlparse

env = lambda e, d: environ[e] if environ.has_key(e) else d
from os import environ

PROJECT_PATH = os.path.split(__file__)[0]

# Add the apps directory to the PYTHONPATH
sys.path.append(os.path.join(PROJECT_PATH, 'apps'))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

BASE_DOMAIN = 'example.com'

ADMINS = (
    ('Thomas Parslow', 'tom@almostobsolete.net'),
)

MANAGERS = ADMINS

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en-GB'

SITE_ID = 1

SITE_URL = 'http://skiffhack.herokuapp.com/'

USE_I18N = False

USE_L10N = False

LOGIN_REDIRECT_URL = '/manage/'

BROWSERID_CREATE_USER = True

STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    ('media', os.path.join(PROJECT_PATH, 'media')),
)

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'staticfiles', 'media')
MEDIA_URL = '/static/media/'

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# The secret key is a heroku env, set with "heroku config:add SECRET_KEY=keyvalue"
SECRET_KEY = env('SECRET_KEY','')

# Default to dummy cache, can be overridden in deployment-specific settings files
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    #    'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    #    'django.middleware.cache.FetchFromCacheMiddleware',
    )

AUTHENTICATION_BACKENDS = (
    'django_browserid.auth.BrowserIDBackend',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django_browserid.context_processors.browserid_form',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
    'gunicorn',
    'django.contrib.auth',
    'django_browserid',  # Load after auth to monkey-patch it.
)
