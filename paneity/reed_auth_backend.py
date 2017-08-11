import ldap3
from django.conf import settings


class ReedAuthBackend(object):
    """
    On a request, it looks for request.META['REMOTE_USER'] and then returns the
    user associated with that username. If that user doesn't exist, it creates
    it based on their data from reed's directory using ldap
    """

    def authenticate(self, request):
        username = request.META.get('REMOTE_USER')
        if username:
            pass


def get_or_create_from_ldap(username):
    """
    based on username it gets the associated user. If that user does
    not exist, it creates it based on their ldap data
    """
    result = {}
    if settings.DEBUG:
        result = {"cn": ["Isabella F Jorissen", "ijorissen"], "eduPersonAffili"
                  "ation": ["student"], "eduPersonEntitlement": ["cascade", "t"
                  "hesis-vpn"], "eduPersonPrimaryAffiliation": "student", "edu"
                  "PersonPrincipalName": "isjoriss@REED.EDU", "gecos": "Isabel"
                  "la F Jorissen", "gidNumber": 503, "givenName": ["Isabella"],
                  "homeDirectory": "/afs/reed.edu/user/i/s/isjoriss", "loginSh"
                  "ell": "/bin/bash", "mail": ["isjoriss@reed.edu"], "objectCl"
                  "ass": ["top", "inetOrgPerson", "eduPerson", "ReedCollegePer"
                          "son", "posixAccount", "inetLocalMailRecipient"],
                  "rcLocalHomeDirectory": "/home/isjoriss", "rcMiddleName":
                  ["F"], "sn": ["Jorissen"], "uid": ["isjoriss"], "uidNumber":
                  39878}
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
