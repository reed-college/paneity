import httplib2
import re
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from base64 import urlsafe_b64encode
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


@login_required(login_url='/admin/login/')
def add_users(request):
    """
    This will use the google api to scrape the user's contact list
    for people with reed emails, then add those people to the db
    with their profile ids.
    """
    # Make sure the user has the permissions to change the db
    if not (request.user.has_perm('auth.add_user') or
            request.user.has_perm('auth.change_user') or
            request.user.has_perm('tutor.add_student') or
            request.user.has_perm('tutor.change_student')):
        return render(request, "error/403.html", status=403)

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
        pageSize=2000,
        requestMask_includeField="person.names,person.email_addresses,person.metadata",
    ).execute()
    connections = results.get('connections', [])

    # Now we add the connections to the db as users
    reedmail = re.compile('.*@reed\.edu$')  # regex that matches reed emails

    # print out every reed email in the connections list
    # and its related profile id
    for con in connections:

        emails = con.get("emailAddresses", [])
        reed_addr = None
        # get reed email
        for email in emails:
            addr = email.get("value", "")
            if addr and reedmail.match(addr):
                reed_addr = addr
        # get profileid
        sources = con.get("metadata", {}).get("sources", [])
        profile_id = None
        for source in sources:
            if source.get("type") == "PROFILE":
                profile_id = source.get("id")
        # get first and last name
        # this gets the first thing in the "names" list
        first_name = con.get("names", [{}])[0].get("givenName")
        last_name = con.get("names", [{}])[0].get("familyName")

        if reed_addr and profile_id and first_name and last_name:
            # @reed.edu is 9 characters
            username = reed_addr[0:-9]
            pw = str(urlsafe_b64encode(os.urandom(6)))[2:10]

            # see if this user already exists
            usr = User.objects.filter(email=reed_addr).first()
            # I'm using .filter and then .first rather than .get
            # because .get throws an error if the user does not
            # exist while .first just returns None
            if usr:
                stu = models.Student.objects.get(user=usr)
            else:
                usr = User.objects.create_user(
                    username,
                    first_name=first_name,
                    last_name=last_name,
                    email=reed_addr,
                    password=pw)
                stu = models.Student.objects.create(user=usr)
            stu.profile_id = profile_id
            usr.save()
            stu.save()

    return HttpResponse("Users were added!")


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
