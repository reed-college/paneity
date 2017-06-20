from django.test import TestCase
from django.urls import reverse
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
