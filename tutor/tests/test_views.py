from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
import tutor.models as models


class IndexTestCase(TestCase):
    """
    Tests for the index view
    """

    def test_index_doesnt_error(self):
        response = self.client.get(reverse('tutor:index'))
        # Assert that its not an error code
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)


class TutorTestCase(TestCase):
    """
    Tests for the tutors view
    """

    def test_tutors_returns_404_for_nonexistant_course(self):
        response = self.client.get(reverse('tutor:tutors', args=[742]))
        self.assertEqual(response.status_code, 404)

    def test_tutors_doesnt_error_on_real_class(self):
        chem = models.Subject.objects.create(
            abbreviation="CHEM",
            name="Chemistry")
        chem.save()
        intro = models.Course.objects.create(
            subject=chem,
            number=101,
            title="Molecular structures")
        intro.save()

        response = self.client.get(reverse('tutor:tutors', args=[intro.id]))
        # Assert that its not an error code
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)


class StartStopTestCase(TestCase):
    """
    Tests for the startstop view
    """

    def test_startstop_doesnt_error(self):
        response = self.client.get(reverse('tutor:startstop'))
        # Assert that its not an error code
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)


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
        # bob doesn't have the right permissions
        response = self.client.get(reverse('tutor:add_users'))
        self.assertEqual(response.status_code, 403)
        bob.delete()

    def test_authorized_user_can_access_add_users(self):
        fred = User.objects.create_user("fred", password="foo")
        # give fred the permissions
        adu = Permission.objects.get(codename='add_user')
        chu = Permission.objects.get(codename='change_user')
        ads = Permission.objects.get(codename='add_student')
        chs = Permission.objects.get(codename='change_student')
        fred.user_permissions.add(adu, chu, ads, chs)
        fred.is_staff = True
        fred.save()
        # have fred access the page
        self.client.login(username="fred", password="foo")
        response = self.client.get(reverse('tutor:add_users'))
        # Assert that its not an error code
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)
        fred.delete()

    def test_superuser_can_access_add_users(self):
        """
        This tests that a superuser can access the add_users page
        This way, if fred can't access the page but jim can, then
        we know the error is with the authorization system
        """
        # jim is going to be a superuser
        jim = User.objects.create_user("jim", password="baz")
        jim.is_staff = True
        jim.is_superuser = True
        jim.save()
        self.client.login(username="jim", password="baz")
        response = self.client.get(reverse('tutor:add_users'))
        # Assert that its not an error code
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)
        jim.delete()
