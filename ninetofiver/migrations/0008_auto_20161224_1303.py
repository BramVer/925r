# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-24 13:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ninetofiver', '0007_auto_20161221_2150'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='holiday',
            unique_together=set([('name', 'date', 'country')]),
        ),
    ]
