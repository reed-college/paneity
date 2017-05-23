from django.conf.urls import url

from . import views

urlpatterns = [
	#ex: /tutor/ ------ This is the Main Page of the app, courses will be listed here
    url(r'^$', views.index, name='index'),
    
    # ex: /tutor/admin/  ------- Page for the admin of the app/site
    url(r'^admin/$', views.admin, name='admin'),
    
    # ex: /tutor/tutors/  --------- Page listing tutors 
    url(r'^tutors/$', views.tutors, name='tutors'),

    # ex: /tutor/startstop/  ------- Page with start and stop button to begin/end tutoring sessions
    url(r'^startstop/$', views.startstop, name='startstop'),
]



