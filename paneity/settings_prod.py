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
