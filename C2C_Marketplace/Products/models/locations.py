from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # Latitude ranges from -90 to 90 degrees
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],
    )
    # Longitude ranges from -180 to 180 degrees
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )

    def __str__(self):
        return f"{self.state}, {self.country}"