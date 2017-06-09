from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('tutor.urls', namespace='tutor')),
    url(r'^admin/', admin.site.urls),
    url(r'^forum/', include('spirit.urls')), #added a namespace for Spirit
]
