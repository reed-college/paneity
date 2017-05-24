from django.test import TestCase
from django.contrib.auth.models import User
import random

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
    Tests for the subject model
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


class StudentTestCase(TestCase):
    """
    Tests for the Student model
    """

    def setUp(self):
        bob = User.objects.create_user('bob', password='bar')
        models.Student.objects.create(user=bob)

    def test_student_can_store_profile_id(self):
        """
        Google profile IDs are integers, but they are larger than
        64 bits. This test makes sure that the database can actually
        store these things.
        My profile ID is a 21 digit number, so I'm going to test
        with another 21 digit number.
        """
        profile_id = random.randint(
            100000000000000000000,
            999999999999999999999)

        bob = User.objects.get(username="bob")
        stu = models.Student.objects.get(user=bob)
        stu.profile_id = profile_id
        stu.save()
        self.assertEquals(stu.profile_id, profile_id)
