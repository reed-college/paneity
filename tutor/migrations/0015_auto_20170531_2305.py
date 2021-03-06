# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0014_auto_20170525_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='abbreviation',
            field=models.CharField(help_text='3-4 letter abbreviation (i.e. HUM)', max_length=4),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(help_text='Full name of the subject (i.e. Humanities)', max_length=50),
        ),
    ]
