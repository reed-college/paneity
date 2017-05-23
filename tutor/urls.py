from django.conf.urls import url

from . import views

urlpatterns = [
	#ex: /tutor/ ------ This is the Home Page of the app
    url(r'^$', views.index, name='index'),

    # ex: /tutor/courses/ ---- Page where we list courses that one can get tutored in  
    url(r'^courses/$', views.courses, name='courses'),
    
    # ex: /tutor/admin/  ------- Page for the admin of the app/site
    url(r'^admin/$', views.admin, name='admin'),
    
    # ex: /tutor/tutors/  --------- Page listing tutors 
    url(r'^tutors/$', views.tutors, name='tutors'),

    # ex: /tutor/startstop/  ------- Page with start and stop button to begin/end tutoring sessions
    url(r'^startstop/$', views.startstop, name='startstop'),
]



