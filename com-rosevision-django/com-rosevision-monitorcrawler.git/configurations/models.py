from mfashion_api.extends import UnixTimestampField

__author__ = 'Zephyre'

from django.db import models


class HostConfiguration(models.Model):
    host_key = models.CharField(max_length=128)
    config_data = models.TextField()
    host_data = models.TextField()
    update_time = UnixTimestampField(auto_created=True, auto_updated=True)