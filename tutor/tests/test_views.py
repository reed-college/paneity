from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AddUsersTestCase(TestCase):
    """
    Tests for the add_users view
    """

    def test_makes_you_log_in(self):
        """
        Makes sure that you have to log in to the view before
        adding users
        by that, I mean that it just checks if the page redirects
        you
        """
        response = self.client.get(reverse('tutor:add_users'))
        self.assertEqual(response.status_code, 302)

    def test_unauthorized_user_cant_add(self):
        """
        Tests that if you're logged in but unauthorized, then you
        get a 403
        """
        bob = User.objects.create_user("bob", password="bar")
        bob.save()
        self.client.login(username="bob", password="bar")
        response = self.client.get(reverse('tutor:add_users'))
        self.assertEqual(response.status_code, 403)
