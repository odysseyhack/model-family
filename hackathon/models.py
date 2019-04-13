from django.db import models

# Create your models here.
class Building(models.Model):
    bag_number = models.CharField(max_length=16)
    building_year = models.IntegerField()
    developer = models.CharField(max_length=256)
    total_score = models.DecimalField(max_digits=10, decimal_places=2)

class PropertyGroup(models.Model):
    property_name = models.CharField(max_length=60)

class BuildingProperty(models.Model):
    title = models.CharField(max_length=60)
    score_weight = models.DecimalField(max_digits=10, decimal_places=2)
    building = models.ManyToManyField(Building)
    expiration_date = models.DateTimeField()
    property_group = models.ForeignKey(PropertyGroup, on_delete=models.CASCADE)

class BuildingOwner(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    bsn_number = models.IntegerField()
    buildings = models.ManyToManyField(Building)

class BuildingMutator(models.Model):
    company_name = models.CharField(max_length=60)
    property_groups = models.ManyToManyField(PropertyGroup)


