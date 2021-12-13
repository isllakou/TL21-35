from django.db import models

# Create your models here.

class Charge(models.Model):
    tagID = models.DecimalField(
        primary_key=True,
        unique=True, 
        max_digits=18, decimal_places=0)
    operatorDebited = models.DecimalField(max_digits=10, decimal_places=0)
    dateOfCharge = models.DateField(auto_now=False)
    vehicleID = models.DecimalField(max_digits=10, decimal_places=0)
    amount = models.DecimalField(
        max_digits=5, decimal_places=2)

    def __repr__(self):
        return self.tagID