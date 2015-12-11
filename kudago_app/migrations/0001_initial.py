# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('external_id', models.IntegerField()),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('stage_theatre', models.CharField(max_length=100, null=True, blank=True)),
                ('price', models.NullBooleanField()),
                ('kids', models.NullBooleanField()),
                ('age_restricted', models.SmallIntegerField(null=True, blank=True)),
                ('run_time', models.SmallIntegerField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(related_name='person_set', to='kudago_app.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.AddField(
            model_name='eventperson',
            name='person',
            field=models.ForeignKey(related_name='event_set', to='kudago_app.Person'),
        ),
        migrations.AddField(
            model_name='eventperson',
            name='role',
            field=models.ForeignKey(related_name='event_persons_set', to='kudago_app.Role'),
        ),
        migrations.AddField(
            model_name='event',
            name='gallery',
            field=models.ManyToManyField(related_name='events', to='kudago_app.Image'),
        ),
        migrations.AddField(
            model_name='event',
            name='persons',
            field=models.ManyToManyField(related_name='events', through='kudago_app.EventPerson', to='kudago_app.Person'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(related_name='events', to='kudago_app.Tag'),
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ForeignKey(related_name='events', to='kudago_app.EventType'),
        ),
    ]
