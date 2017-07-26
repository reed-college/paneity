import sys, os

cwd = os.getcwd()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

INTERP = os.path.expanduser("~/venv/bin/python")
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0,'$HOME/venv/bin')
sys.path.insert(0,'$HOME/venv/lib/python3.4/site-packages/django')
sys.path.insert(0,'$HOME/venv/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paneity.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
