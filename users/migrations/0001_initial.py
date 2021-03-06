# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-25 20:49
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='users', max_length=30)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('avatar', models.ImageField(blank=True, default='/static/images/default-avatar.png', null=True, upload_to='uploads/%Y/%m/%d')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True, validators=(django.core.validators.RegexValidator('^[+]?\\d{9,15}$', message='Số điện thoại không hợp lệ'),))),
                ('allergy', models.TextField(blank=True, max_length=100, null=True)),
                ('point', models.PositiveIntegerField(default=0)),
                ('address', models.TextField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=30, null=True)),
                ('district', models.CharField(blank=True, max_length=30, null=True)),
                ('ward', models.CharField(blank=True, max_length=30, null=True)),
                ('is_chef', models.BooleanField(default=False)),
                ('info', models.TextField(blank=True, null=True)),
                ('avatar_link', models.URLField(blank=True, default='', null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
