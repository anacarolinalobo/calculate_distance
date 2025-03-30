from django.db import models

class DistanceQuery(models.Model):
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance_km = models.FloatField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"""'source': {self.source},
            'destination': {self.destination},
            'distance': {self.distance_km} km,
            'created_at': `{self.created_at}"""
