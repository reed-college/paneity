from django.test import TestCase
from datetime import datetime
from random import randint
import tutor.templatetags.tutor_extras as tutor_extras
from tutor.util import random_string


class GetVcLinkTestCase(TestCase):
    """
    Tests for the get_vc_link function
    """

    def test_order_of_usernames_doesnt_matter(self):
        """
        Makes sure that the same two usernames passed in different
        orders produces the same link
        """
        username1 = random_string(randint(8, 100))
        username2 = random_string(randint(8, 100))
        link1 = tutor_extras.get_vc_link(username1, username2)
        link2 = tutor_extras.get_vc_link(username2, username1)
        self.assertEqual(link1, link2)

    def test_uniqueness_of_links(self):
        """
        This tests a bunch of usernames and sees if two different
        pairs of usernames generate the same link
        """
        username1 = random_string(randint(8, 100))
        username2 = random_string(randint(8, 100))
        for i in range(0, 100):
            username3 = random_string(randint(8, 100))
            username4 = random_string(randint(8, 100))
            link1 = tutor_extras.get_vc_link(username1, username2)
            link2 = tutor_extras.get_vc_link(username3, username4)
            if (username1 != username3) and (username1 != username4) and (username2 != username3) and (username3 != username4):
                # if there is a collision, with will print out the
                # usernames with the error message
                try:
                    self.assertNotEqual(link1, link2)
                except AssertionError as e:
                    message = "{}\nusername1: {}\nusername2: {}\nusername3: {}\nusername4: {}"
                    message = message.format(e,
                                             username1,
                                             username2,
                                             username3,
                                             username4)
                    raise(AssertionError(message))

            username1 = username3
            username2 = username4


class DatetimeGeTestCase(TestCase):
    """
    tests on the datetime_ge function
    """

    def test_that_one_date_is_greater_than_other(self):
        """
        Pretty silly test, but it will make sure that the function
        has basic functionaliy and doesn't get imported incorectly
        """
        dt1 = datetime(1980, 1, 1)
        dt2 = datetime(1990, 1, 1)
        self.assertTrue(tutor_extras.datetime_ge(dt2, dt1))
