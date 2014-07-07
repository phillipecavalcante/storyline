# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class Article(models.Model):

    source = models.CharField(max_length=255)
    url = models.URLField()
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=False)
    description = models.TextField()
    body = models.TextField()
    links = models.TextField()

    def __unicode__(self):
        return "%s - %s" % (self.id, self.title)

class Topic(models.Model):

    name = models.CharField(max_length=255)
    terms = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
