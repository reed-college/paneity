from django.test import TestCase
import uuid
import tutor.templatetags.tutor_extras as tutor_extras


class GetVcLinkTestCase(TestCase):
    """
    Tests for the get_vc_link function
    """

    def test_order_of_usernames_doesnt_matter(self):
        """
        Makes sure that the same two usernames passed in different
        orders produces the same link
        """
        username1 = uuid.uuid4()
        username2 = uuid.uuid4()
        link1 = tutor_extras.get_vc_link(username1, username2)
        link2 = tutor_extras.get_vc_link(username2, username1)
        self.assertEqual(link1, link2)
