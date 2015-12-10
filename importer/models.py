from django.db import models


class Type(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.slug


class Tag(models.Model):
    name = models.CharField(max_length=140)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Image(models.Model):
    url = models.URLField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.url


"""
    Events
"""


class EventType(Type):
    pass


class EventTag(Tag):
    pass


class EventImage(Image):
    pass


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    role = models.OneToOneField(Role)

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.role)


class EventPerson(models.Model):
    pass


class Event(models.Model):
    external_id = models.IntegerField()

    title = models.CharField(max_length=100)
    text = models.TextField()
    description = models.TextField()
    stage_theatre = models.CharField(max_length=100)

    price = models.NullBooleanField()
    kids = models.NullBooleanField()

    age_restricted = models.SmallIntegerField()
    run_time = models.SmallIntegerField()

    tags = models.ManyToManyField('EventTag', related_name='events')
    persons = models.ManyToManyField('Person', related_name='events')
    type = models.OneToOneField(EventType)
    gallery = models.ForeignKey(EventImage)


class Places(models.Model):
    pass


class Schedule(models.Model):
    pass
