from django.conf.urls import url

from . import views

urlpatterns = [
    # courses will be listed here
    url(r'^$', views.index, name='index'),
    # ex: tutoring/1/tutors/  --------- Page listing tutors and
    # office hours for a given course
    url(r'^(?P<course_id>[0-9]+)/tutors/$', views.tutors, name='tutors'),
    # ex: tutoring/inbox/  --------- This page displays the most recent messages from
    # each person you've talked to
    url(r'^inbox/$', views.inbox, name='inbox'),
    # ex: tutoring/about/  --------- Page detailing who made this webapp and
    # through which program at Reed
    url(r'^about/$', views.about, name='about'),
]
