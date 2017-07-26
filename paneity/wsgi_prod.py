"""
For production, you should change the wsgi.py symbolic link to point to this
file instead of wsgi_dev.py
"""
import sys
import os
from django.core.wsgi import get_wsgi_application

cwd = os.getcwd()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INTERP = os.path.expanduser("~/venv/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, '$HOME/venv/bin')
sys.path.insert(0, '$HOME/venv/lib/python3.4/site-packages/django')
sys.path.insert(0, '$HOME/venv/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paneity.settings_prod")
application = get_wsgi_application()
