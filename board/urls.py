from django.conf.urls import url

import board.views as views

urlpatterns = [
    url(r'^(?P<subject_id>[0-9]+)/list/$', views.list, name='list'),
]
