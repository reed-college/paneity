from django.test import TestCase
from django.contrib.auth.models import User
import random

import tutor.models as models
from spirit.category.models import Category


class CourseTestCase(TestCase):
    """
    Tests for the Course model
    """

    def setUp(self):
        _make_hum()

    def tearDown(self):
        _delete_hum()

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

    def test_subject_delete_deletes_category_as_well(self):
        """
        This tests that when you delete a subject it deletes the
        category associated with that subject
        """
        lit = models.Subject.objects.create(
            abbreviation="LIT", name="Literature")
        cat_id = lit.category.id
        lit.delete()
        self.assertFalse(Category.objects.filter(id=cat_id).exists())

    def test_subject_queryset_delete_deletes_category(self):
        """
        Same as the above test but does a queryset delete. This is
        important because the admin interface uses queryset deletes
        """
        lit = models.Subject.objects.create(
            abbreviation="LIT", name="Literature")
        cat_id = lit.category.id
        subs = models.Subject.objects.filter(id=lit.id)
        subs.delete()
        self.assertFalse(Category.objects.filter(id=cat_id).exists())


class StudentTestCase(TestCase):
    """
    Tests for the Student model
    """

    def setUp(self):
        bob = User.objects.create_user('bob', password='bar')
        models.Student.objects.create(user=bob)
        _make_hum()

    def tearDown(self):
        bob = User.objects.get(username='bob')
        bob.delete()
        _delete_hum()

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

    def test_student_that_tutors_a_class_is_a_tutor(self):
        """
        Makes sure that when you add a tutoring class to a student,
        the server makes that student a tutor
        """
        bob = User.objects.get(username="bob")
        stu = models.Student.objects.get(user=bob)
        hum110 = models.Course.objects.get(
            number=110,
            title="Ancient Mediterranean")
        stu.tutoring_classes.add(hum110)
        stu.save()
        self.assertTrue(stu.tutor)


def _make_hum():
    """
    Makes HUM subject and Hum110 course
    """
    hum = models.Subject.objects.create(
        abbreviation="HUM",
        name="Humanities")
    models.Course.objects.create(
        subject=hum,
        number=110,
        title="Ancient Mediterranean")


def _delete_hum():
    """
    deletes hum and hum 110
    """
    hum110 = models.Course.objects.get(
        number=110,
        title="Ancient Mediterranean")
    hum110.delete()
    hum = models.Subject.objects.get(
        abbreviation="HUM",
        name="Humanities")
    hum.delete()
