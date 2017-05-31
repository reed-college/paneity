from django.test import TestCase
from django.contrib.auth.models import User
import tutor.util as util


class AddConnectionsTestCase(TestCase):

    def test_dummy_connections_get_added(self):
        """
        pretty basic test, just runs add_connections on a hard-coded
        connections list and checks that the connections are in the
        db
        """
        connections = [
            {
                'resourceName': 'people/c349234092380923483',
                'metadata': {'sources': [{
                    'type': 'PROFILE',
                    'id': '341307096764789717159',
                    'etag': '#4eZz2/IuMFw=',
                    'profileMetadata': {'objectType': 'PERSON'},
                }], 'objectType': 'PERSON'},
                'names': [{
                    'metadata': {'primary': True,
                                 'source': {'type': 'PROFILE',
                                            'id': '341307096764789717159'}
                                 },
                    'displayName': 'John Smith',
                    'familyName': 'Smith',
                    'givenName': 'John',
                    'displayNameLastFirst': 'Smith, John',
                }],
                'emailAddresses': [{'value': 'smithjo@reed.edu'}],
            },
        ]
        util.add_connections(connections)
        john = User.objects.get(email="smithjo@reed.edu")
        self.assertEqual(john.first_name, "John")
        self.assertEqual(john.last_name, "Smith")
