from django.db import models

# Create your models here.

from django.db import models

class SmartPhone(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    display_size = models.FloatField(blank=True, null=True)
    storage_capacity = models.PositiveIntegerField(blank=True, null=True)
    camera_resolution = models.PositiveIntegerField(blank=True, null=True)
    battery_capacity = models.PositiveIntegerField(blank=True, null=True)
    operating_system = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    is_water_resistant = models.BooleanField(default=False)
    is_5g_enabled = models.BooleanField(default=False)
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name
class TV(models.Model):
    name = models.CharField(max_length=70)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    display_size = models.FloatField(blank=True, null=True)
    isSmartTV = models.BooleanField(default=False)
    weight = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.name
