from django.db import models
from django.contrib.gis.db import models

class Vessel(models.Model):
    id = models.AutoField(primary_key=True)
    vessel_id = models.BigIntegerField(null=True, blank=True)
    received_time_utc = models.DateField()
    geo_location = models.PointField(srid=4326, null=False, blank=False)