# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-25 20:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, default='')),
                ('rating', models.IntegerField(choices=[(1, 'One star'), (2, 'Two stars'), (3, 'Three stars'), (4, 'Four stars'), (5, 'Five stars')], default=4)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('approved_comment', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='item.Item')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserProfile')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('item', 'reviewer')]),
        ),
    ]
