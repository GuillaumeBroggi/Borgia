# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-18 19:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='is_displayed',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_read',
        ),
    ]
