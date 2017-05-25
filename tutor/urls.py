from django.conf.urls import url

from . import views

urlpatterns = [
	#ex: /tutor/ ------ This is the Main Page of the app, courses will be listed here
    url(r'^$', views.index, name='index'),
    
    # ex: /tutor/1/tutors/  --------- Page listing tutors
    url(r'^(?P<course_id>[0-9]+)/tutors/$', views.tutors, name='tutors'),

    # ex: /tutor/startstop/  ------- Page with start and stop button to begin/end tutoring sessions
    url(r'^startstop/$', views.startstop, name='startstop'),
]
