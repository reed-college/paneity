from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from apiclient import discovery
from oauth2client import client

import tutor.models as models


def index(request):
    return render(
        request,
        'tutor/index.html',
        {"Courses": list(models.Course.objects.all())})


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


def add_users(request):
    """
    This will use the google api to scrape the user's contact list
    for people with reed emails, then add those people to the db
    with their profile ids.
    """
    credentials = request.session.get("credentials")
    if credentials is None:
        return redirect('oauth2callback')
    return HttpResponse(request.session.keys())


def oauth2callback(request):
    """
    callback for google api stuff
    """
    return HttpResponse("Hi")
