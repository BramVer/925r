# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 14:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('ninetofiver', '0006_auto_20161215_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmploymentContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('legal_country', django_countries.fields.CountryField(max_length=2)),
                ('started_at', models.DateField()),
                ('ended_at', models.DateField(blank=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ninetofiver.Company')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_ninetofiver.employmentcontract_set+', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
