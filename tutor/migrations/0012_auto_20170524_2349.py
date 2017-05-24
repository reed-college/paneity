# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0011_auto_20170524_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='tutoring_classes',
            field=models.ManyToManyField(blank=True, help_text='The courses that this student can tutor in.', null=True, to='tutor.Course'),
        ),
    ]