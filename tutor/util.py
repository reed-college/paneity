"""
place for functions that will be used in other files
"""
import random
import string
import ldap3
from django.conf import settings


def random_string(n):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))


def get_or_create(username):
    """
    based on username it gets the associated user. If that user does
    not exist, it creates it based on their ldap data
    """
    result = {}
    if settings.DEBUG:
        result = {"cn": ["Isabella F Jorissen","ijorissen"],"eduPersonAffiliation": ["student"],"eduPersonEntitlement": ["cascade","thesis-vpn"],"eduPersonPrimaryAffiliation": "student","eduPersonPrincipalName": "isjoriss@REED.EDU","gecos": "Isabella F Jorissen","gidNumber": 503,"givenName": ["Isabella"],"homeDirectory": "/afs/reed.edu/user/i/s/isjoriss","loginShell": "/bin/bash","mail": ["isjoriss@reed.edu"],"objectClass": ["top","inetOrgPerson","eduPerson","ReedCollegePerson","posixAccount","inetLocalMailRecipient"],"rcLocalHomeDirectory": "/home/isjoriss","rcMiddleName": ["F"],"sn": ["Jorissen"],"uid": ["isjoriss"],"uidNumber": 39878}
    else:
        server = ldap3.Server('ldap.reed.edu', port=389, get_info=ldap3.ALL)
        con = ldap3.Connection(server, auto_bind=True)
        query = 'uid={!s},ou=people,dc=reed,dc=edu'.format(username)
        con.search(
            search_base=query,
            search_filter='(objectClass=*)',
            search_scope=ldap3.SUBTREE,
            attributes=ldap3.ALL_ATTRIBUTES)
        result = con.response[0]['attributes']

    return result
