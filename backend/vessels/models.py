from django.db import models
from django.contrib.gis.db import models as geo

class Vessel(models.Model):
    id = models.AutoField(primary_key=True)
    vessel_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['vessel_id'], name='vessel_id_idx')
        ]

    def __str__(self):
        return "%s" % (self.vessel_id)

class Location(models.Model):
    received_time_utc = models.DateTimeField(null=False, blank=False)
    geo_location = geo.PointField(srid=4326, null=False, blank=False)
    vessel = models.ForeignKey(
        Vessel, 
        related_name="locations", 
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        indexes = [
            models.Index(fields=['received_time_utc'], name='received_time_utc_idx')
        ]
    
    def __str__(self):
        return "Vessel %s (%s)" % (self.vessel.vessel_id, self.received_time_utc)