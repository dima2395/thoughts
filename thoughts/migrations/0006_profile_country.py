# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 14:34
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('thoughts', '0005_remove_profile_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
