# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 10:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kudago_app', '0002_auto_20151211_0459'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('time_till', models.TimeField(blank=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='kudago_app.Event')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='kudago_app.Place')),
            ],
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
