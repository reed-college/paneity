from django.test import TestCase
import tutor.models as models


class CourseTestCase(TestCase):
    """
    Tests for the Course model
    """

    def setUp(self):
        hum = models.Subject.objects.create(
            abbreviation="HUM",
            name="Humanities")
        models.Course.objects.create(
            subject=hum,
            number=110,
            title="Ancient Mediterranean")

    def test_course_model_has_useful_string(self):
        """
        Makes sure that the course model string function has something to do
        with the actual object. More specififcally, it asserts that either
        the title or number appears in the string.
        """
        hum110 = models.Course.objects.get(
            number=110,
            title="Ancient Mediterranean")
        self.assertTrue((hum110.title in hum110.__str__())
                        or (str(hum110.number) in hum110.__str__()))


class SubjectTestCase(TestCase):
    """
    Tests for the Course model
    """

    def setUp(self):
        models.Subject.objects.create(abbreviation="HUM", name="Humanities")

    def test_course_model_has_useful_string(self):
        """
        Makes sure that the subject model string function has something to
        do with the actual object. More specififcally, it asserts that either
        the name or abbreviation appears in the string.
        """
        hum = models.Subject.objects.get(abbreviation="HUM", name="Humanities")
        self.assertTrue((hum.name in hum.__str__())
                        or (hum.abbreviation in hum.__str__()))
