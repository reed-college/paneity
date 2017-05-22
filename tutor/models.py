from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """
    Profile model for additional info about students
    Right now it just stores whether or not a user is a tutor
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tutor = models.BooleanField(default=False)


class Subject(models.Model):
    """
    Subject that course can be taught in (i.e. Math, Humanities)
    """
    abbreviation = models.CharField(max_length=4, help_text="3-4 letter abbreviation for a subject (i.e. HUM)")
    name = models.CharField(max_length=50, help_text="full name of the subject (i.e. Humanities)")


class Course(models.Model):
    """
    model for a single course that people can tutor in
    """
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE,)
    number = models.IntegerField()
    title = models.CharField(max_length=100, help_text="(i.e. Ancient Mediterranean, or Intro to Economic Analysis)")
