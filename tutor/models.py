from django.db import models
from django.contrib.auth.models import User
from django import forms
from spirit.category.models import Category

class Student(models.Model):
    """
    Profile model for additional info about students
    Right now it just stores whether or not a user is a tutor
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutor = models.BooleanField(default=False)
    tutoring_classes = models.ManyToManyField(
        'Course',
        blank=True,
        related_name="tutors",
        help_text="The courses that this student can tutor in.")
    enrolled_classes = models.ManyToManyField(
        'Course',
        blank=True,
        related_name="students",
        help_text="The courses that this student is currently enrolled in.")
    profile_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="ProfileID for Google People API")


class Subject(models.Model):
    """
    Subject that course can be taught in (i.e. Math, Humanities)
    """
    abbreviation = models.CharField(
        max_length=4,
        help_text="3-4 letter abbreviation (i.e. HUM)")
    name = models.CharField(
        max_length=50,
        help_text="Full name of the subject (i.e. Humanities)")
        # below we are creating a one-to-one relationship between Subjects and Categories, so that the forum is structured
        # around Reed's departments, not arbitrary categories.
    category = models.OneToOneField(Category, on_delete=models.CASCADE, null=True, blank=True)
    def save(self, *args, **kwargs):
        for field_name in ['abbreviation', 'name']:
            val = getattr(self, field_name, False)
            if field_name == 'abbreviation':
                setattr(self, 'abbreviation', val.upper())
            elif field_name == 'name':
                setattr(self, 'name', val.capitalize())
        cat = Category.objects.create(title=self.name)
        cat.save()
        self.category = cat

        super(Subject, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class Course(models.Model):
    """
    model for a single course that people can tutor in
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,)
    number = models.IntegerField()
    title = models.CharField(
        max_length=100,
        help_text="(i.e. Ancient Mediterranean, or Intro to Economic Analysis)")

    def __str__(self):
        return "{} {}".format(self.subject.abbreviation, self.number)
