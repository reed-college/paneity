from django.test import TestCase
import tutor.models as models


class CourseTestCase(TestCase):
    """
    Tests for the Course model
    """

    def setUp(self):
        hum = models.Subject.objects.create(abbreviation="HUM", name="Humanities")
        models.Course.objects.create(subject=hum, number=110, title="Ancient Mediterranean")

    def test_course_model_has_string(self):
        """
        Makes sure that the course model has string function so that it will have a name
        attached to it on the Admin site
        """
        hum110 = models.Course.objects.get(number=110, title="Ancient Mediterranean")
        self.assertNotEqual(hum110.__str__(), "")
