"""
gapi.py
This is the file for the views that use the google api
"""
import httplib2
from apiclient import discovery
from oauth2client import client

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import tutor.util as util


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
        return redirect('tutor:oauth2callback')
    credentials = client.OAuth2Credentials.from_json(credentials)
    if credentials.access_token_expired:
        return redirect('tutor:oauth2callback')

    # Now we get the contacts from the user
    http = credentials.authorize(httplib2.Http())
    service = discovery.build(
        'people',
        'v1',
        http=http,
        discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')

    # Loop through the pages of connections
    next_page_token = ""
    while next_page_token is not None:
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            pageToken=next_page_token,
            requestMask_includeField="person.names,person.email_addresses,person.metadata",
        ).execute()
        connections = results.get('connections', [])

        # Now we add the connections to the db as users
        util.add_connections(connections)

        next_page_token = results.get("nextPageToken")

    return HttpResponse("Users were added!")


def oauth2callback(request):
    """
    callback for google api stuff
    """
    flow = client.flow_from_clientsecrets(
        'client_secrets.json',
        scope='https://www.googleapis.com/auth/contacts.readonly',
        redirect_uri=request.build_absolute_uri(reverse('tutor:oauth2callback')))
    if 'code' not in request.GET:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.GET.get('code')
        credentials = flow.step2_exchange(auth_code)
        request.session['credentials'] = credentials.to_json()
        return redirect('tutor:add_users')
