from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # This redirects to the urlpatterns in spirit.urls
    # This makes the spirit forum our homepage
    url(r'^', include('spirit.urls')),
    # This page allows admins to create new users, new courses,
    # new subjects, etc
    url(r'^admin/', admin.site.urls),
    # This redirects to tutoring urls
    url(r'^tutoring/', include('tutor.urls', namespace='tutor')),
    # This redirects to django private chat urls, and this doesn't
    # interfere with the first url()
    # because django looks at them in order from first to last
    url(r'^', include('django_private_chat.urls')),
]
