from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

PROJECT_APPS = [
	'app.apps.AppConfig',
	'api.apps.ApiConfig',
	'rest_framework.authtoken',
]

PROJECT_MIDDLEWARE = [
]

INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE = PREREQ_MIDDLEWARE + PROJECT_MIDDLEWARE

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'moments',
	    'HOST': 'localhost',
	    'USER': 'root',
		'PASSWORD': 'root',
	    'PORT': 3306
    }
}
#
# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.sqlite3',
# 		'NAME': 'db.sqlite3'
# 	}
# }

