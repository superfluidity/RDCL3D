# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-12 01:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_generated', models.DateTimeField()),
                ('date_received', models.DateTimeField(default=django.utils.timezone.now)),
                ('body', jsonfield.fields.JSONField(default={})),
                ('request_meta', jsonfield.fields.JSONField(default={})),
                ('status', models.CharField(choices=[(1, 'Unprocessed'), (2, 'Processed'), (3, 'Error')], default=1, max_length=250)),
            ],
        ),
    ]
