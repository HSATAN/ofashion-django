"""
Django settings for mfashion_api project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6l_#19$%e5u^-t4llu0^1zl#z3y14tozy5+_ks#ccorxtldia5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sellers',
    'products',
    'configurations',
    'web',
    'tags',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'mfashion_api.urls'

WSGI_APPLICATION = 'mfashion_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASE_ROUTERS = ['web.router.AuthRouter', 'web.router.ProductsRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mfashion_api',
        # 'USER': 'spider',
        # 'PASSWORD': 'R$b8uPhA3eTr',
        # 'HOST': '121.201.8.91',
        'USER': 'root',
        'PASSWORD': 'mfashion',
        'HOST': '121.201.15.204',
        'PORT': '3306',
    },
    'celery_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'celery',
        # 'USER': 'select',
        # 'PASSWORD': 'mfashionselect',
        # 'HOST': '121.201.8.91',
        'USER': 'rose',
        'PASSWORD': 'rose123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
    'products_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'products_core',
        # 'USER': 'rose',
        # 'PASSWORD': 'rose123',
        # 'HOST': '121.201.8.91',
        'USER': 'root',
        'PASSWORD': 'mfashion',
        'HOST': '121.201.15.204',
        'PORT': '3306',
    },

}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh_CN'

TIME_ZONE = 'Asia/Shanghai'
DEFAULT_CHARSET = 'UTF-8'
USE_I18N = True

USE_L10N = True

USE_TZ = False

SEARCH_ENGINE_URL = 'http://localhost:8983/solr'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), '../static').replace("\\", '/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'tags/templates'),
)

LOGIN_REDIRECT_URL = '/'
