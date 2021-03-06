from django.db import models
from taggit.managers import TaggableManager


STATUS = (
    ('W', 'Waiting'),
    ('I', 'Init'),
    ('D', 'Done'),
    ('R', 'Running'),
    ('F', 'Failed'),
)


class VagrantBox(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=120)
    boxname = models.CharField(max_length=120)
    description = models.JSONField(blank=True, null=True)
    tags = TaggableManager(blank=True)  # https://django-taggit.readthedocs.io/en/latest/api.html#filtering

    processed_at = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    status_code = models.CharField(max_length=10, choices=STATUS, blank=True, null=True)
    status_message = models.TextField(blank=True, null=True)
    worker_name = models.CharField(max_length=50, blank=True, null=True)
    #results_code =
    #result_message =


class VagrantPoolLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status_code = models.CharField(max_length=10, choices=STATUS)
    status_message = models.TextField(blank=True, null=True)
    vagrant_box = models.ForeignKey(VagrantBox, on_delete=models.CASCADE)
    worker_name = models.CharField(max_length=50, blank=True, null=True)


# !!! use only by 'overseer.functions.addMoreToQueue()'
class SearchBacklog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    pagenumber = models.SmallIntegerField()
    keyword = models.CharField(max_length=50, blank=True, null=True)
    worker_name = models.CharField(max_length=50, blank=True, null=True)
    status_code = models.CharField(max_length=10, choices=STATUS, blank=True, null=True)
    status_message = models.TextField(blank=True, null=True)


class Indicator():
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.SmallIntegerField()  # 0 debug, 1 info, 2 warn, 3 alert, 4 confirmed
    category = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    splunk_query = models.CharField(max_length=1000, blank=True, null=True)


class IndicatorFireLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    severity = models.SmallIntegerField()  # 0 debug, 1 info, 2 warn, 3 alert, 4 confirmed


