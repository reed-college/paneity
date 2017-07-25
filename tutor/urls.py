from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: / ------ This is the Main Page of the app, courses will be listed here
    url(r'^$', views.index, name='index'),

    # ex: /1/tutors/  --------- Page listing tutors
    url(r'^(?P<course_id>[0-9]+)/tutors/$', views.tutors, name='tutors'),
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^about/$', views.about, name='about'),
]
