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


class EventPerson(models.Model):
    event = models.ForeignKey('Event', related_name='person_set')
    person = models.ForeignKey('Person', related_name='event_set')
    role = models.ForeignKey('Role', related_name='event_persons_set')

    def __unicode__(self):
        return '%s - %s(%s)' % (self.event, self.person, self.role)


# Places


class PlaceType(Type):
    pass


class WorkTimeType(Type):
    pass


class Place(models.Model):
    external_id = models.IntegerField()

    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=140, )

    url = models.URLField(null=True, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    type = models.ForeignKey('PlaceType', related_name='places')
    city = models.ForeignKey('City', related_name='places')

    metros = models.ManyToManyField('Subway', related_name='places')
    tags = models.ManyToManyField('Tag', related_name='places')
    gallery = models.ManyToManyField('Image', related_name='places')
    phones = models.ManyToManyField('Phone', related_name='places')
    work_times = models.ManyToManyField('WorkTime', related_name='places')


class City(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Subway(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('City', related_name='metros')

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.city)


class Phone(models.Model):
    phone = models.CharField(max_length=30)

    def __unicode__(self):
        return self.phone


class WorkTime(models.Model):
    time = models.CharField(max_length=140)
    type = models.ForeignKey('WorkTimeType', related_name='work_time')

    def __unicode__(self):
        return '%s (%s)' % (self.time, self.type)



class Schedule(models.Model):
    pass