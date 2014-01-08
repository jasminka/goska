from settings import *

DEBUG = 1#False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'goska',
        'USER': 'miha02',
        'PASSWORD': 'BD6ET3vnyK3YeYvP',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

ALLOWED_HOSTS = ['.goska.si']
