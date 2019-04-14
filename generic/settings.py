"""
Django settings for hackathon project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
from generic import allowed_hosts_settings
from generic import auth_password_validators
from generic import installed_apps_settings
from generic import logging_settings
from generic import middleware_settings
from generic import templates_settings

LOGGING = logging_settings.LOGGING
TEMPLATES = templates_settings.TEMPLATES
MIDDLEWARE = middleware_settings.MIDDLEWARE
AUTH_PASSWORD_VALIDATORS = auth_password_validators.AUTH_PASSWORD_VALIDATORS
ALLOWED_HOSTS = allowed_hosts_settings.ALLOWED_HOSTS
INSTALLED_APPS = installed_apps_settings.INSTALLED_APPS
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '98fim!5fs6&coov+o1lk$!p9=x^92*0r*#rxgu7n=u5yr3(77j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}

CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
)

ROOT_URLCONF = 'generic.urls'

WSGI_APPLICATION = 'generic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'site_static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


ENABLE_USER_ACTIVATION = True
DISABLE_USERNAME = False
LOGIN_VIA_EMAIL = False
LOGIN_VIA_EMAIL_OR_USERNAME = True
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'log_in'
USE_REMEMBER_ME = True

RESTORE_PASSWORD_VIA_EMAIL_OR_USERNAME = False
ENABLE_ACTIVATION_AFTER_EMAIL_CHANGE = True

SIGN_UP_FIELDS = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
if DISABLE_USERNAME:
    SIGN_UP_FIELDS = ['first_name', 'last_name', 'email', 'password1', 'password2']

os.environ['HTTPS'] = "on"
