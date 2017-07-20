from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
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


class TutorChatTestCase(TestCase):

    def test_redirects_if_not_logged_in(self):
        """
        The page should redirect you if you're not logged in
        """
        response = self.client.get(reverse('tutor:tutorchat'))
        self.assertEqual(response.status_code, 302)

    def test_normal_user_can_access_page(self):
        """
        Makes sure that non-tutors can login
        """
        bob = User.objects.create_user("bob", password="bar")
        bob.save()
        self.client.login(username="bob", password="bar")
        # bob doesn't have the right permissions
        response = self.client.get(reverse('tutor:tutorchat'))
        self.assertEqual(response.status_code, 200)
        bob.delete()

    def test_student_can_access_page(self):
        """
        This just checks that if you are a use with a student object,
        you can access the page
        """
        johnny = User.objects.create_user("johnny", password="foo")
        johnny.save()
        models.Student.objects.create(user=johnny)
        self.client.login(username="johnny", password="foo")
        response = self.client.get(reverse('tutor:tutorchat'))
        self.assertEqual(response.status_code, 200)
        johnny.delete()

    def test_tutor_can_access_page(self):
        """
        Tutors should be able to access the page
        """
        mark = User.objects.create_user("mark", password="ohhai")
        mark.save()
        stu = models.Student.objects.create(user=mark)
        stu.tutor = True
        stu.save()
        self.client.login(username="mark", password="ohhai")
        response = self.client.get(reverse('tutor:tutorchat'))
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)
        mark.delete()

    def test_superuser_can_access_page(self):
        """
        Super Users should be able to access the page
        """
        lisa = User.objects.create_user("lisa", password="tear")
        lisa.is_superuser = True
        lisa.save()
        self.client.login(username="lisa", password="tear")
        response = self.client.get(reverse('tutor:tutorchat'))
        self.assertTrue(response.status_code < 400)
        self.assertTrue(response.status_code >= 200)
        lisa.delete()
