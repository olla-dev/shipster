from django.db import models
from django.contrib.gis.db import models as geo

class Vessel(models.Model):
    vessel_id = models.BigIntegerField(unique=True, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['vessel_id', 'id'], name='vessel_id_idx')
        ]
        ordering = ['-vessel_id']

    def __str__(self):
        return "%s" % (self.vessel_id)

class Location(models.Model):
    received_time_utc = models.DateTimeField(null=False, blank=False)
    point = geo.PointField(srid=4326, null=False, blank=False)
    vessel = models.ForeignKey(
        Vessel, 
        related_name="locations", 
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=['received_time_utc', 'id'], name='received_time_utc_idx')
        ]
        ordering = ['-received_time_utc']
    
    def __str__(self):
        return "Vessel %s (%s)" % (self.vessel.vessel_id, self.received_time_utc)