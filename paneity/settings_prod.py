"""
This file gets set as the default settings by paneity/wsgi_prod.py and
thats how those settings go in to effect
"""
from paneity.settings import *

with open('secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'paneity'
    }
}

# Login url and logout url
LOGIN_URL = "https://weblogin.reed.edu/?cosign-halp"
LOGOUT_URL = "/logout"

# Stuff for django_private_chat
CHAT_WS_SERVER_HOST = 'halp.reed.edu'
CHAT_WS_SERVER_PORT = 5002
