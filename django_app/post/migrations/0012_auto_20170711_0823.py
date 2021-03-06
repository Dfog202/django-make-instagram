# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-11 08:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0011_auto_20170627_0342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='create_date',
            new_name='created_date',
        ),
        migrations.AlterUniqueTogether(
            name='postlike',
            unique_together=set([('post', 'user')]),
        ),
    ]
