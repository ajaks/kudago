# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kudago_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(null=True, blank=True)),
                ('address', models.CharField(max_length=140)),
                ('url', models.URLField(null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('city', models.ForeignKey(related_name='places', to='kudago_app.City')),
                ('gallery', models.ManyToManyField(related_name='places', to='kudago_app.Image')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(related_name='metros', to='kudago_app.City')),
            ],
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='WorkTimeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Places',
        ),
        migrations.AddField(
            model_name='worktime',
            name='type',
            field=models.ForeignKey(related_name='work_time', to='kudago_app.WorkTimeType'),
        ),
        migrations.AddField(
            model_name='place',
            name='metros',
            field=models.ManyToManyField(related_name='places', to='kudago_app.Subway'),
        ),
        migrations.AddField(
            model_name='place',
            name='phones',
            field=models.ManyToManyField(related_name='places', to='kudago_app.Phone'),
        ),
        migrations.AddField(
            model_name='place',
            name='tags',
            field=models.ManyToManyField(related_name='places', to='kudago_app.Tag'),
        ),
        migrations.AddField(
            model_name='place',
            name='type',
            field=models.ForeignKey(related_name='places', to='kudago_app.PlaceType'),
        ),
        migrations.AddField(
            model_name='place',
            name='work_times',
            field=models.ManyToManyField(related_name='places', to='kudago_app.WorkTime'),
        ),
    ]
