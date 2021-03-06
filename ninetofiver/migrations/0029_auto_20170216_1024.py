# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-16 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ninetofiver', '0028_auto_20170215_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=255, unique=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_ninetofiver.contractgroup_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='projectgroup',
            name='polymorphic_ctype',
        ),
        migrations.AlterUniqueTogether(
            name='projectgrouping',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='projectgrouping',
            name='group',
        ),
        migrations.RemoveField(
            model_name='projectgrouping',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='projectgrouping',
            name='project',
        ),
        migrations.AlterUniqueTogether(
            name='usergrouping',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='usergrouping',
            name='group',
        ),
        migrations.RemoveField(
            model_name='usergrouping',
            name='polymorphic_ctype',
        ),
        migrations.RemoveField(
            model_name='usergrouping',
            name='user',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_groups',
            field=models.ManyToManyField(blank=True, to='ninetofiver.UserGroup'),
        ),
        migrations.DeleteModel(
            name='ProjectGroup',
        ),
        migrations.DeleteModel(
            name='ProjectGrouping',
        ),
        migrations.DeleteModel(
            name='UserGrouping',
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_groups',
            field=models.ManyToManyField(blank=True, to='ninetofiver.ContractGroup'),
        ),
    ]
