from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import User
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


class DialogsTestCase(TestCase):
    """
    Tests for the dialogs view of django-private-chat
    """

    def setUp(self):
        jim = User.objects.create_user("jim", password="baz")
        jim.save()
        fred = User.objects.create_user("fred", password="foo")
        fred.save()

    def tearDown(self):
        jim = User.objects.get(username="jim")
        fred = User.objects.get(username="fred")
        jim.delete()
        fred.delete()

    def test_dialogs_doesnt_error(self):
        self.client.login(username="jim", password="baz")
        response = self.client.get(reverse('dialogs_detail', args=['fred']))
        # Assert that its not an error code
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)
