from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^tutor/', include('tutor.urls', namespace='tutor')),
    url(r'^board/', include('board.urls', namespace='board')),
    url(r'^admin/', admin.site.urls),
]
