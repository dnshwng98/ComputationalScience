from django.db import models


class Data(models.Model):
    occurrence_time_utc = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    magnitude = models.FloatField()
    depth_km = models.FloatField()
    area = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Data'
        ordering = ('occurrence_time_utc',)
        unique_together = ('occurrence_time_utc', 'latitude', 'longitude')