"""
place for functions that will be used in other files
"""
import re
import os
import random
import string
from base64 import urlsafe_b64encode
from django.contrib.auth.models import User
import tutor.models as models


def random_string(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))


def add_connections(connections):
    """
    Takes a google people api connections list and adds the
    connections that have reed emails to the database.
    it also updates the profile ids on existing users with reed
    emails.
    """
    # regex that matches reed emails
    reedmail = re.compile('.*@reed\.edu$')
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
