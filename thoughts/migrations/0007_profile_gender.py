# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0006_profile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, null=True),
        ),
    ]
