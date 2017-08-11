import ldap3
from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend


class ReedAuthBackend(RemoteUserBackend):
    """
    On a request, it looks for request.META['REMOTE_USER'] and then returns the
    user associated with that username. If that user doesn't exist, it creates
    it based on their data from reed's directory using ldap
    """

    def authenticate(self, request, remote_user):
        # getting the user object that authenticate returns
        user = super().authenticate(request, remote_user)
        # if data about them is not in the db, get it from ldap
        if user:
            if not (user.first_name and user.last_name and user.email):
                username = remote_user
                if user.username:
                    username = user.username
                result = get_ldap_data(username)
                last_name = result.get("sn")
                if last_name:
                    user.last_name = last_name[0]
                first_name = result.get("givenName")
                if first_name:
                    user.first_name = first_name[0]
                email = result.get("mail")
                if email:
                    user.email = email[0]
                user.save()
        return user


def get_ldap_data(username):
    """
    gets data about a username from reed's ldap dictory
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
        server = ldap3.Server(settings.LDAP_ADDRESS,
                              port=settings.LDAP_PORT,
                              get_info=ldap3.ALL)
        con = ldap3.Connection(server, auto_bind=True)
        query = 'uid={!s},ou=people,dc=reed,dc=edu'.format(username)
        con.search(
            search_base=query,
            search_filter='(objectClass=*)',
            search_scope=ldap3.SUBTREE,
            attributes=ldap3.ALL_ATTRIBUTES)
        result = con.response[0]['attributes']

    return result
