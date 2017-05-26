import httplib2
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
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
    # This block makes sure we have the credentials and they're
    # not expired
    credentials = request.session.get("credentials")
    if credentials is None:
        return redirect('oauth2callback')
    credentials = client.OAuth2Credentials.from_json(credentials)
    if credentials.access_token_expired:
        return redirect('oauth2callback')

    # Now we get the contacts from the user
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(
        'people',
        'v1',
        http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=10,
        requestMask_includeField="person.names",
    ).execute()
    connections = results.get('connections', [])

    return HttpResponse(connections)


def oauth2callback(request):
    """
    callback for google api stuff
    """
    print(request.GET)
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/contacts.readonly',
        redirect_uri=request.build_absolute_uri(reverse('oauth2callback')))
    if 'code' not in request.GET:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        request.session['credentials'] = credentials.to_json()
        return redirect('add_users')
