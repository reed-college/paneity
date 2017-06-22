from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: / ------ This is the Main Page of the app, courses will be listed here
    url(r'^$', views.index, name='index'),

    # ex: /1/tutors/  --------- Page listing tutors
    url(r'^(?P<course_id>[0-9]+)/tutors/$', views.tutors, name='tutors'),

    # ex: /startstop/  ------- Page with start and stop button to begin/end tutoring sessions
    url(r'^startstop/$', views.startstop, name='startstop'),

    # ex: /dropin/  ------- Page listing drop-in and office hours
    url(r'^dropin/$', views.dropin, name='dropin'),

    url(r'^add_users/$', views.add_users, name='add_users'),
    url(r'^oauth2callback/$', views.oauth2callback, name='oauth2callback'),
]
