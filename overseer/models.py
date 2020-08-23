from django.db import models
from taggit.managers import TaggableManager


# Create your models here.
class VagrantBox(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    username = models.CharField(max_length=120)
    boxname = models.CharField(max_length=120)
    # vagrantfile =
    description = models.JSONField(blank=True, null=True)
    tags = TaggableManager(blank=True)  # https://django-taggit.readthedocs.io/en/latest/api.html#filtering



class SearchBacklog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    pagenumber = models.SmallIntegerField()