from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^tutor/', include('tutor.urls')),
    url(r'^admin/', admin.site.urls),
]