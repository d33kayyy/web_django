# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-08 09:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_auto_20170212_0005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='pub_date',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='modified_date',
            new_name='updated_date',
        ),
        migrations.AddField(
            model_name='item',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]