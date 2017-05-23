from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

import tutor.models as models


def index(request):
    return HttpResponse("List courses here.")

def admin(request):
    return HttpResponse("This be the admin page.")


def tutors(request, course_id):
    """
    View for the tutors page
    It gets the course based on the course id put in the address bar.
    Then, if the course exists, it renders the tutors.html page and passes
    the list of tutors on that course to the page.
    """
    try:
        course = models.Course.objects.get(pk=course_id)
    except models.Course.DoesNotExist:
        raise Http404("Course does not exist")
    # student_set has the info of all of the users who are marked as tutors
    # for this course
    return render(
        request,
        'tutor/tutors.html',
        {"tutors": course.student_set.all()})


def startstop(request):
    return render(request, 'tutor/startstop.html')
