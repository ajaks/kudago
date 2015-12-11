from django.db import models


class Type(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.slug


class Tag(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return self.name


class Image(models.Model):
    url = models.URLField()

    def __unicode__(self):
        return self.url


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

"""
    Events
"""


class EventType(Type):
    pass


class EventPerson(models.Model):
    event = models.ForeignKey('Event', related_name='person_set')
    person = models.ForeignKey('Person', related_name='event_set')
    role = models.ForeignKey('Role', related_name='event_persons_set')

    def __unicode__(self):
        return '%s - %s(%s)' % (self.event, self.person, self.role)


class Event(models.Model):
    external_id = models.IntegerField()

    title = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stage_theatre = models.CharField(max_length=100, blank=True, null=True)

    price = models.NullBooleanField()
    kids = models.NullBooleanField()

    age_restricted = models.SmallIntegerField(blank=True, null=True)
    run_time = models.SmallIntegerField(blank=True, null=True)

    tags = models.ManyToManyField('Tag', related_name='events')
    persons = models.ManyToManyField('Person', through='EventPerson', related_name='events')
    type = models.ForeignKey(EventType, related_name='events')
    gallery = models.ManyToManyField('Image', related_name='events')


class Places(models.Model):
    pass


class Schedule(models.Model):
    pass